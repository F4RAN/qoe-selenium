#!/usr/bin/env python3
"""
Copyright 2017-2018 Deutsche Telekom AG, Technische Universität Berlin, Technische
Universität Ilmenau, LM Ericsson

Permission is hereby granted, free of charge, to use the software for research
purposes.

Any other use of the software, including commercial use, merging, publishing,
distributing, sublicensing, and/or selling copies of the Software, is
forbidden. For a commercial license, please contact the respective rights
holders of the standards ITU-T Rec. P.1203, ITU-T Rec. P.1203.1, ITU-T Rec.
P.1203.2, and ITU-T Rec. P.1203.3. See https://www.itu.int/en/ITU-T/ipr/Pages/default.aspx
for more information.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import math
from functools import lru_cache

import numpy as np

from . import log, utils
from .errors import P1203StandaloneError
from .measurementwindow import MeasurementWindow

logger = log.setup_custom_logger("itu_p1203")


class P1203Pv(object):
    _COEFFS = {
        "u1": 72.61,
        "u2": 0.32,
        "t1": 30.98,
        "t2": 1.29,
        "t3": 64.65,
        "q1": 4.66,
        "q2": -0.07,
        "q3": 4.06,
        "mode0": {
            "a1": 11.9983519,
            "a2": -2.99991847,
            "a3": 41.2475074001,
            "a4": 0.13183165961,
        },
        "mode1": {
            "a1": 5.00011566,
            "a2": -1.19630824,
            "a3": 41.3585049,
            "a4": 0,
            "c0": -0.91562479,
            "c1": 0,
            "c2": -3.28579526,
            "c3": 20.4098663,
        },
        "htv_1": -0.60293,
        "htv_2": 2.12382,
        "htv_3": -0.36936,
        "htv_4": 0.03409,
    }

    def degradation_due_to_upscaling(self, coding_res, display_res):
        """
        Degradation due to upscaling
        """
        scale_factor = display_res / coding_res
        scale_factor = max(scale_factor, 1)
        u1 = self.coeffs["u1"]
        u2 = self.coeffs["u2"]
        deg_scal_v = u1 * np.log10(u2 * (scale_factor - 1.0) + 1.0)
        deg_scal_v = utils.constrain(deg_scal_v, 0.0, 100.0)
        return deg_scal_v

    def degradation_due_to_frame_rate_reduction(self, deg_cod_v, deg_scal_v, framerate):
        """
        Degradation due to frame rate reduction
        """
        t1 = self.coeffs["t1"]
        t2 = self.coeffs["t2"]
        t3 = self.coeffs["t3"]
        deg_frame_rate_v = 0
        if framerate < 24:
            deg_frame_rate_v = (
                (100 - deg_cod_v - deg_scal_v)
                * (t1 - t2 * framerate)
                / (t3 + framerate)
            )
        deg_frame_rate_v = utils.constrain(deg_frame_rate_v, 0.0, 100.0)
        return deg_frame_rate_v

    def degradation_integration(
        self, mos_cod_v, deg_cod_v, deg_scal_v, deg_frame_rate_v
    ):
        """
        Integrate the three degradations
        """
        deg_all = utils.constrain(deg_cod_v + deg_scal_v + deg_frame_rate_v, 0.0, 100.0)
        qv = 100 - deg_all
        return utils.mos_from_r(qv)

    @lru_cache()
    def video_model_function_mode0(
        self, coding_res, display_res, bitrate_kbps_segment_size, framerate
    ):
        """
        Mode 0 model

        Arguments:
            coding_res {int} -- number of pixels in coding resolution
            display_res {int} -- number of display resolution pixels
            bitrate_kbps_segment_size {float} -- bitrate in kBit/s
            framerate {float} -- frame rate

        Returns:
            float -- O22 score
        """

        # compression degradation
        a1 = self.coeffs["mode0"]["a1"]
        a2 = self.coeffs["mode0"]["a2"]
        a3 = self.coeffs["mode0"]["a3"]
        a4 = self.coeffs["mode0"]["a4"]
        q1 = self.coeffs["q1"]
        q2 = self.coeffs["q2"]
        q3 = self.coeffs["q3"]
        quant = a1 + a2 * np.log(
            a3
            + np.log(bitrate_kbps_segment_size)
            + np.log(
                bitrate_kbps_segment_size
                * bitrate_kbps_segment_size
                / (coding_res * framerate)
                + a4
            )
        )
        mos_cod_v = q1 + q2 * np.exp(q3 * quant)
        mos_cod_v = utils.constrain(mos_cod_v, 1.0, 5.0)
        deg_cod_v = 100.0 - utils.r_from_mos(mos_cod_v)
        deg_cod_v = utils.constrain(deg_cod_v, 0.0, 100.0)

        # scaling, framerate degradation
        deg_scal_v = self.degradation_due_to_upscaling(coding_res, display_res)
        deg_frame_rate_v = self.degradation_due_to_frame_rate_reduction(
            deg_cod_v, deg_scal_v, framerate
        )

        # degradation integration
        score = self.degradation_integration(
            mos_cod_v, deg_cod_v, deg_scal_v, deg_frame_rate_v
        )

        logger.debug(
            json.dumps(
                {
                    "coding_res": round(coding_res, 2),
                    "display_res": round(display_res, 2),
                    "bitrate_kbps_segment_size": round(bitrate_kbps_segment_size, 2),
                    "framerate": round(framerate, 2),
                    "mos_cod_v": round(mos_cod_v, 2),
                    "deg_cod_v": round(deg_cod_v, 2),
                    "deg_scal_v": round(deg_scal_v, 2),
                    "deg_frame_rate_v": round(deg_frame_rate_v, 2),
                    "score": round(score, 2),
                },
                indent=True,
            )
        )

        return score

    def video_model_function_mode1(
        self,
        coding_res,
        display_res,
        bitrate_kbps_segment_size,
        framerate,
        frames,
        iframe_ratio=None,
    ):
        """
        Mode 1 model

        Arguments:
            coding_res {int} -- number of pixels in coding resolution
            display_res {int} -- number of display resolution pixels
            bitrate_kbps_segment_size {float} -- bitrate in kBit/s
            framerate {float} -- frame rate
            frames {list} -- frames
            iframe_ratio {float} -- iframe ratio, only for debugging

        Returns:
            float -- O22 score
        """
        # compression degradation
        a1 = self.coeffs["mode1"]["a1"]
        a2 = self.coeffs["mode1"]["a2"]
        a3 = self.coeffs["mode1"]["a3"]
        a4 = self.coeffs["mode1"]["a4"]
        q1 = self.coeffs["q1"]
        q2 = self.coeffs["q2"]
        q3 = self.coeffs["q3"]
        quant = a1 + a2 * np.log(
            a3
            + np.log(bitrate_kbps_segment_size)
            + np.log(
                bitrate_kbps_segment_size
                * bitrate_kbps_segment_size
                / (coding_res * framerate)
                + a4
            )
        )
        mos_cod_v = q1 + q2 * np.exp(q3 * quant)
        mos_cod_v = utils.constrain(mos_cod_v, 1.0, 5.0)

        # if iframe ratio is already set (debug mode)

        # complexity correction
        c0 = self.coeffs["mode1"]["c0"]
        c1 = self.coeffs["mode1"]["c1"]
        c2 = self.coeffs["mode1"]["c2"]
        c3 = self.coeffs["mode1"]["c3"]
        if not iframe_ratio:
            i_sizes = []
            noni_sizes = []
            for frame in frames:
                frame_size = utils.calculate_compensated_size(
                    frame["type"], frame["size"], frame["dts"]
                )
                if frame["type"] == "I":
                    i_sizes.append(int(frame_size))
                else:
                    noni_sizes.append(int(frame_size))

            # only compute ratio when there are frames of both types
            if i_sizes and noni_sizes:
                iframe_ratio = np.mean(i_sizes) / np.mean(noni_sizes)
            else:
                iframe_ratio = 0
        complexity = utils.sigmoid(c0, c1, c2, c3, iframe_ratio)
        mos_cod_v += complexity

        deg_cod_v = 100.0 - utils.r_from_mos(mos_cod_v)
        deg_cod_v = utils.constrain(deg_cod_v, 0.0, 100.0)

        # scaling, framerate degradation
        deg_scal_v = self.degradation_due_to_upscaling(coding_res, display_res)
        deg_frame_rate_v = self.degradation_due_to_frame_rate_reduction(
            deg_cod_v, deg_scal_v, framerate
        )

        # degradation integration
        score = self.degradation_integration(
            mos_cod_v, deg_cod_v, deg_scal_v, deg_frame_rate_v
        )

        logger.debug(
            json.dumps(
                {
                    "coding_res": round(coding_res, 2),
                    "display_res": round(display_res, 2),
                    "bitrate_kbps_segment_size": round(bitrate_kbps_segment_size, 2),
                    "framerate": round(framerate, 2),
                    "mos_cod_v": round(mos_cod_v, 2),
                    "deg_cod_v": round(deg_cod_v, 2),
                    "iframe_ratio": round(iframe_ratio, 2),
                    "complexity": round(complexity, 2),
                    "deg_scal_v": round(deg_scal_v, 2),
                    "deg_frame_rate_v": round(deg_frame_rate_v, 2),
                    "score": round(score, 2),
                },
                indent=True,
            )
        )

        return score

    def video_model_function_mode2(
        self,
        coding_res,
        display_res,
        framerate,
        frames,
        quant=None,
        avg_qp_per_noni_frame=[],
    ):
        """
        Mode 2 model

        Arguments:
            coding_res {int} -- number of pixels in coding resolution
            display_res {int} -- number of display resolution pixels
            framerate {float} -- frame rate
            frames {list} -- frames
            quant {float} -- quant parameter, only used for debugging [default: None]
            avg_qp_per_noni_frame {list} -- average QP per non-I frame, only used for debugging [default: []]
        Returns:
            float -- O22 score
        """

        if not quant:
            if not avg_qp_per_noni_frame:
                types = []
                qp_values = []
                for frame in frames:
                    qp_values.append(frame["qpValues"])
                    frame_type = frame["type"]
                    if frame_type not in ["I", "P", "B", "Non-I"]:
                        raise P1203StandaloneError(
                            "frame type "
                            + str(frame_type)
                            + " not valid; must be I/P/B or I/Non-I"
                        )
                    types.append(frame_type)

                qppb = []
                for index, frame_type in enumerate(types):
                    if frame_type in ["P", "B", "Non-I"]:
                        qppb.extend(qp_values[index])
                avg_qp = np.mean(qppb)
            else:
                avg_qp = np.mean(avg_qp_per_noni_frame)
            quant = avg_qp / 51.0

        q1 = self.coeffs["q1"]
        q2 = self.coeffs["q2"]
        q3 = self.coeffs["q3"]

        mos_cod_v = q1 + q2 * math.exp(q3 * quant)
        mos_cod_v = max(min(mos_cod_v, 5), 1)
        deg_cod_v = 100 - utils.r_from_mos(mos_cod_v)
        deg_cod_v = max(min(deg_cod_v, 100), 0)

        # scaling, framerate degradation
        deg_scal_v = self.degradation_due_to_upscaling(coding_res, display_res)
        deg_frame_rate_v = self.degradation_due_to_frame_rate_reduction(
            deg_cod_v, deg_scal_v, framerate
        )

        # degradation integration
        score = self.degradation_integration(
            mos_cod_v, deg_cod_v, deg_scal_v, deg_frame_rate_v
        )

        logger.debug(
            json.dumps(
                {
                    "coding_res": round(coding_res, 2),
                    "display_res": round(display_res, 2),
                    "framerate": round(framerate, 2),
                    "quant": round(quant, 2),
                    "mos_cod_v": round(mos_cod_v, 2),
                    "deg_cod_v": round(deg_cod_v, 2),
                    "deg_scal_v": round(deg_scal_v, 2),
                    "deg_frame_rate_v": round(deg_frame_rate_v, 2),
                    "score": round(score, 2),
                },
                indent=True,
            )
        )

        return score

    def video_model_function_mode3(
        self,
        coding_res,
        display_res,
        framerate,
        frames,
        quant=None,
        avg_qp_per_noni_frame=[],
    ):
        """
        Mode 3 model

        Arguments:
            coding_res {int} -- number of pixels in coding resolution
            display_res {int} -- number of display resolution pixels
            framerate {float} -- frame rate
            frames {list} -- frames
            quant {float} -- quant parameter, only used for debugging [default: None]
            avg_qp_per_noni_frame {list} -- average QP per non-I frame, only used for debugging [default: []]
        Returns:
            float -- O22 score
        """

        if not quant:
            # iterate through all frames and collect information
            if not avg_qp_per_noni_frame:
                types = []
                qp_values = []
                for frame in frames:
                    qp_values.append(frame["qpValues"])
                    frame_type = frame["type"]
                    if frame_type not in ["I", "P", "B", "Non-I"]:
                        raise P1203StandaloneError(
                            "frame type "
                            + str(frame_type)
                            + " not valid; must be I/P/B or I/Non-I"
                        )
                    types.append(frame_type)

                qppb = []
                for index, frame_type in enumerate(types):
                    if frame_type in ["P", "B", "Non-I"]:
                        qppb.extend(qp_values[index])
                    elif frame_type == "I" and len(qppb) > 0:
                        if len(qppb) > 1:
                            # replace QP value of last P-frame before I frame with QP value of previous P-frame if there
                            # are more than one stored P frames
                            qppb[-1] = qppb[-2]
                        else:
                            # if there is only one stored P frame before I-frame, remove it
                            qppb = []
                avg_qp = np.mean(qppb)
            else:
                avg_qp = np.mean(avg_qp_per_noni_frame)
            quant = avg_qp / 51.0

        q1 = self.coeffs["q1"]
        q2 = self.coeffs["q2"]
        q3 = self.coeffs["q3"]

        mos_cod_v = q1 + q2 * math.exp(q3 * quant)
        mos_cod_v = max(min(mos_cod_v, 5), 1)
        deg_cod_v = 100 - utils.r_from_mos(mos_cod_v)
        deg_cod_v = max(min(deg_cod_v, 100), 0)

        # scaling, framerate degradation
        deg_scal_v = self.degradation_due_to_upscaling(coding_res, display_res)
        deg_frame_rate_v = self.degradation_due_to_frame_rate_reduction(
            deg_cod_v, deg_scal_v, framerate
        )

        # degradation integration
        score = self.degradation_integration(
            mos_cod_v, deg_cod_v, deg_scal_v, deg_frame_rate_v
        )

        logger.debug(
            json.dumps(
                {
                    "coding_res": round(coding_res, 2),
                    "display_res": round(display_res, 2),
                    "framerate": round(framerate, 2),
                    "quant": round(quant, 2),
                    "mos_cod_v": round(mos_cod_v, 2),
                    "deg_cod_v": round(deg_cod_v, 2),
                    "deg_scal_v": round(deg_scal_v, 2),
                    "deg_frame_rate_v": round(deg_frame_rate_v, 2),
                    "score": round(score, 2),
                },
                indent=True,
            )
        )

        return score

    def handheld_adjustment(self, score):
        """
        Compensate for mobile viewing devices.
        """
        # clause 8.4.1 eq. (13)
        htv_1 = self.coeffs["htv_1"]
        htv_2 = self.coeffs["htv_2"]
        htv_3 = self.coeffs["htv_3"]
        htv_4 = self.coeffs["htv_4"]
        return max(
            min(htv_1 + htv_2 * score + htv_3 * score**2 + htv_4 * score**3, 5), 1
        )

    def model_callback(self, output_sample_timestamp, frames):
        """
        Function that receives frames from measurement window, to call the model
        on and produce scores.

        Arguments:
            output_sample_timestamp {int} -- timestamp of the output sample (1, 2, ...)
            frames {list} -- list of all frames from measurement window
        """
        logger.debug("Output score at timestamp " + str(output_sample_timestamp))
        output_sample_index = [
            i for i, f in enumerate(frames) if f["dts"] < output_sample_timestamp
        ][-1]

        if self.mode == 0:
            if any("representation" in f for f in frames):
                frames = utils.get_chunk(frames, output_sample_index, type="video")
                first_frame = frames[0]
                bitrate = np.mean([f["bitrate"] for f in frames])
                display_res = first_frame.get("displaySize") or self.display_res
                score = self.video_model_function_mode0(
                    utils.resolution_to_number(first_frame["resolution"]),
                    utils.resolution_to_number(display_res),
                    bitrate,
                    first_frame["fps"],
                )
            else:
                score = self.video_model_function_mode0(
                    utils.resolution_to_number(
                        frames[output_sample_index]["resolution"]
                    ),
                    utils.resolution_to_number(
                        frames[output_sample_index].get("displaySize")
                        or self.display_res
                    ),
                    frames[output_sample_index]["bitrate"],
                    frames[output_sample_index]["fps"],
                )
        else:
            # only get the relevant frames from the chunk
            frames = utils.get_chunk(frames, output_sample_index, type="video")
            first_frame = frames[0]
            display_res = first_frame.get("displaySize") or self.display_res
            if self.mode == 1:
                # average the bitrate based on the frame sizes, as implemented
                # in submitted model code
                compensated_sizes = [
                    utils.calculate_compensated_size(f["type"], f["size"], f["dts"])
                    for f in frames
                ]
                duration = np.sum([f["duration"] for f in frames])
                bitrate = np.sum(compensated_sizes) * 8 / duration / 1000
                score = self.video_model_function_mode1(
                    utils.resolution_to_number(first_frame["resolution"]),
                    utils.resolution_to_number(display_res),
                    bitrate,
                    first_frame["fps"],
                    frames,
                )
            elif self.mode == 2:
                score = self.video_model_function_mode2(
                    utils.resolution_to_number(first_frame["resolution"]),
                    utils.resolution_to_number(display_res),
                    first_frame["fps"],
                    frames,
                )
            elif self.mode == 3:
                score = self.video_model_function_mode3(
                    utils.resolution_to_number(first_frame["resolution"]),
                    utils.resolution_to_number(display_res),
                    first_frame["fps"],
                    frames,
                )
            else:
                raise P1203StandaloneError("Unsupported mode: {}".format(self.mode))

        # mobile adjustments
        if self.device in ["mobile", "handheld"]:
            score = self.handheld_adjustment(score)

        self.o22.append(score)

    def check_codec(self):
        """check if the segments are using valid codecs,
        in P1203 only h264 is allowed
        """
        codecs = list(set([s["codec"] for s in self.segments]))
        for c in codecs:
            if c != "h264":
                raise P1203StandaloneError("Unsupported codec: {}".format(c))

    def _calculate_with_measurementwindow(self):
        """
        Calculate the score with the measurement window (standardized) approach.
        """

        measurementwindow = MeasurementWindow()
        measurementwindow.set_score_callback(self.model_callback)

        # check which mode can be run
        # TODO: make this switchable by command line option
        self.mode = 0
        for segment in self.segments:
            if "frames" not in segment.keys():
                self.mode = 0
                break
            if "frames" in segment:
                for frame in segment["frames"]:
                    if (
                        "frameType" not in frame.keys()
                        or "frameSize" not in frame.keys()
                    ):
                        raise P1203StandaloneError(
                            "Frame definition must have at least 'frameType' and 'frameSize'"
                        )
                    if "qpValues" in frame.keys():
                        self.mode = 3
                    else:
                        self.mode = 1
                        break

        logger.debug("Evaluating stream in mode " + str(self.mode))

        # check for differing or wrong codecs
        self.check_codec()

        # generate fake frames
        if self.mode == 0:
            dts = 0
            for segment in self.segments:
                num_frames = int(segment["duration"] * segment["fps"])
                frame_duration = 1.0 / segment["fps"]
                for i in range(int(num_frames)):
                    frame = {
                        "duration": frame_duration,
                        "dts": dts,
                        "bitrate": segment["bitrate"],
                        "codec": segment["codec"],
                        "fps": segment["fps"],
                        "resolution": segment["resolution"],
                    }
                    if "displaySize" in segment.keys():
                        frame["displaySize"] = segment["displaySize"]
                    if "representation" in segment.keys():
                        frame.update({"representation": segment["representation"]})
                    # feed frame to MeasurementWindow
                    measurementwindow.add_frame(frame)
                    dts += frame_duration
            measurementwindow.stream_finished()

        # use frame info to infer frames and their DTS, add frame stats
        else:
            dts = 0
            for segment_index, segment in enumerate(self.segments):
                num_frames_assumed = int(segment["duration"] * segment["fps"])
                num_frames = len(segment["frames"])
                if num_frames != num_frames_assumed:
                    logger.warning(
                        "Segment specifies "
                        + str(num_frames)
                        + " frames but based on calculations, there should be "
                        + str(num_frames_assumed)
                    )
                frame_duration = 1.0 / segment["fps"]
                for i in range(int(num_frames)):
                    frame = {
                        "duration": frame_duration,
                        "dts": dts,
                        "bitrate": segment["bitrate"],
                        "codec": segment["codec"],
                        "fps": segment["fps"],
                        "resolution": segment["resolution"],
                        "size": segment["frames"][i]["frameSize"],
                        "type": segment["frames"][i]["frameType"],
                    }
                    if "displaySize" in segment.keys():
                        frame["displaySize"] = segment["displaySize"]
                    if "representation" in segment.keys():
                        frame.update({"representation": segment["representation"]})
                    if self.mode == 3:
                        qp_values = segment["frames"][i]["qpValues"]
                        if not qp_values:
                            raise P1203StandaloneError(
                                "No QP values for frame {i} of segment {segment_index}".format(
                                    **locals()
                                )
                            )
                        frame["qpValues"] = qp_values
                    # feed frame to MeasurementWindow
                    measurementwindow.add_frame(frame)
                    dts += frame_duration
            measurementwindow.stream_finished()

    def _calculate_fast_mode(self):
        """
        Calculate the score using the fast mode.
        This calculates one O22 value per chunk and repeats it for floor(s) where s = segment duration.
        """
        # check which mode can be run
        if self.mode is not None and self.mode != 0:
            raise P1203StandaloneError(
                f"Fast mode only works with mode 0, but it is set to {self.mode}"
            )

        self.mode = 0

        for segment in self.segments:
            score = self.video_model_function_mode0(
                utils.resolution_to_number(segment["resolution"]),
                utils.resolution_to_number(self.display_res),
                segment["bitrate"],
                segment["fps"],
            )
            self.o22.extend([score] * math.floor(segment["duration"]))

    def calculate(self, fast_mode=False):
        """
        Calculate video MOS

        Returns:
            dict {
                "video": {
                    "streamId": i13["streamId"],
                    "mode": mode,
                    "O22": o22,
                }
            }

        Parameters:
            fast_mode {bool} -- if True, use the fast mode of the model (less precise)
        """

        utils.check_segment_continuity(self.segments, "video")

        if fast_mode:
            logger.warning(
                "Using fast mode of the model, results may not be accurate to the second"
            )
            self._calculate_fast_mode()
        else:
            self._calculate_with_measurementwindow()

        return {
            "video": {
                "streamId": self.stream_id,
                "mode": self.mode,
                "O22": self.o22,
            }
        }

    def __init__(
        self, segments, display_res="1920x1080", device="pc", stream_id=None, coeffs={}
    ):
        """
        Initialize Pv model with input JSON data

        Arguments:
            segments {list} -- list of segments according to specification
            display_res {str} -- display resolution as "wxh" (default: "1920x1080")
            device {str} -- "pc" or "mobile" (default: "pc")
            stream_id {str} -- stream ID (default: {None})
            coeffs {dict} -- model coefficients, will overwrite defaults if same key is used [default: {}]
        """
        self.segments = segments
        self.display_res = display_res
        self.device = device
        self.stream_id = stream_id
        self.o22 = []
        self.mode = None
        # update possible new coeffs that are passed in the method
        self.coeffs = {**self._COEFFS, **coeffs}


if __name__ == "__main__":
    print("this is just a module")
