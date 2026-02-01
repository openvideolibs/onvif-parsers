import typing

from onvif_parsers import model, registry, util

# TODO: this file should not exist. None of these have unit tests because they were
# added before the unit test framework was in place. They should be moved to individual
# files categorized by manufacturer or functionality and have unit tests added.
# DO NOT add new parsers to this file.


@registry.register("tns1:VideoSource/ImageTooBlurry/AnalyticsService")
@registry.register("tns1:VideoSource/ImageTooBlurry/ImagingService")
@registry.register("tns1:VideoSource/ImageTooBlurry/RecordingService")
async def async_parse_image_too_blurry(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing image too blurry detection."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Image Too Blurry",
        "binary_sensor",
        "problem",
        None,
        payload.Data.SimpleItem[0].Value == "true",
        "diagnostic",
    )


@registry.register("tns1:VideoSource/ImageTooDark/AnalyticsService")
@registry.register("tns1:VideoSource/ImageTooDark/ImagingService")
@registry.register("tns1:VideoSource/ImageTooDark/RecordingService")
async def async_parse_image_too_dark(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle image too dark detection."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Image Too Dark",
        "binary_sensor",
        "problem",
        None,
        payload.Data.SimpleItem[0].Value == "true",
        "diagnostic",
    )


@registry.register("tns1:VideoSource/ImageTooBright/AnalyticsService")
@registry.register("tns1:VideoSource/ImageTooBright/ImagingService")
@registry.register("tns1:VideoSource/ImageTooBright/RecordingService")
async def async_parse_image_too_bright(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle image too bright detection."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Image Too Bright",
        "binary_sensor",
        "problem",
        None,
        payload.Data.SimpleItem[0].Value == "true",
        "diagnostic",
    )


@registry.register("tns1:VideoSource/GlobalSceneChange/AnalyticsService")
@registry.register("tns1:VideoSource/GlobalSceneChange/ImagingService")
@registry.register("tns1:VideoSource/GlobalSceneChange/RecordingService")
async def async_parse_scene_change(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle global scene change detection."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Global Scene Change",
        "binary_sensor",
        "problem",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:AudioAnalytics/Audio/DetectedSound")
async def async_parse_detected_sound(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle sound detected event."""
    audio_source = ""
    audio_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "AudioSourceConfigurationToken":
            audio_source = source.Value
        if source.Name == "AudioAnalyticsConfigurationToken":
            audio_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    return model.EventEntity(
        f"{uid}_{topic}_{audio_source}_{audio_analytics}_{rule}",
        "Detected Sound",
        "binary_sensor",
        "sound",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:RuleEngine/FieldDetector/ObjectsInside")
async def async_parse_field_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing field detector events."""
    video_source = ""
    video_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "VideoAnalyticsConfigurationToken":
            video_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}_{video_analytics}_{rule}",
        "Field Detection",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:RuleEngine/CellMotionDetector/Motion")
async def async_parse_cell_motion_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing cell motion detector events."""
    video_source = ""
    video_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "VideoAnalyticsConfigurationToken":
            video_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}_{video_analytics}_{rule}",
        "Cell Motion Detection",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:RuleEngine/MotionRegionDetector/Motion")
async def async_parse_motion_region_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing motion region detector events."""
    video_source = ""
    video_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "VideoAnalyticsConfigurationToken":
            video_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}_{video_analytics}_{rule}",
        "Motion Region Detection",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value in ["1", "true"],
    )


@registry.register("tns1:RuleEngine/TamperDetector/Tamper")
async def async_parse_tamper_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing tamper detector events."""
    video_source = ""
    video_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "VideoAnalyticsConfigurationToken":
            video_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}_{video_analytics}_{rule}",
        "Tamper Detection",
        "binary_sensor",
        "problem",
        None,
        payload.Data.SimpleItem[0].Value == "true",
        "diagnostic",
    )


@registry.register("tns1:RuleEngine/MyRuleDetector/DogCatDetect")
async def async_parse_dog_cat_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing pet detection event for dog/cat."""
    video_source = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "Source":
            video_source = util.normalize_video_source(source.Value)

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}",
        "Pet Detection",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:RuleEngine/MyRuleDetector/VehicleDetect")
async def async_parse_vehicle_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing vehicle detection event."""
    video_source = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "Source":
            video_source = util.normalize_video_source(source.Value)

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}",
        "Vehicle Detection",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:RuleEngine/MyRuleDetector/PeopleDetect")
async def async_parse_person_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing person detection event."""
    video_source = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "Source":
            video_source = util.normalize_video_source(source.Value)

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}",
        "Person Detection",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:RuleEngine/MyRuleDetector/FaceDetect")
async def async_parse_face_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing face detection event."""
    video_source = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "Source":
            video_source = util.normalize_video_source(source.Value)

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}",
        "Face Detection",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:RuleEngine/MyRuleDetector/Visitor")
async def async_parse_visitor_detector(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing visitor detection event."""
    video_source = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "Source":
            video_source = util.normalize_video_source(source.Value)

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}",
        "Visitor Detection",
        "binary_sensor",
        "occupancy",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:Device/Trigger/DigitalInput")
async def async_parse_digital_input(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing digital input events."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Digital Input",
        "binary_sensor",
        None,
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )


@registry.register("tns1:Device/Trigger/Relay")
async def async_parse_relay(uid: str, msg: typing.Any) -> model.EventEntity | None:
    """Handle parsing relay trigger events."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Relay Triggered",
        "binary_sensor",
        None,
        None,
        payload.Data.SimpleItem[0].Value == "active",
    )


@registry.register("tns1:Device/HardwareFailure/StorageFailure")
async def async_parse_storage_failure(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing storage failure events."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Storage Failure",
        "binary_sensor",
        "problem",
        None,
        payload.Data.SimpleItem[0].Value == "true",
        "diagnostic",
    )


@registry.register("tns1:Monitoring/ProcessorUsage")
async def async_parse_processor_usage(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing processor usage events."""
    topic, payload = util.extract_message(msg)
    usage = float(payload.Data.SimpleItem[0].Value)
    if usage <= 1:
        usage *= 100

    return model.EventEntity(
        f"{uid}_{topic}",
        "Processor Usage",
        "sensor",
        None,
        "percent",
        int(usage),
        "diagnostic",
    )


@registry.register("tns1:Monitoring/OperatingTime/LastReboot")
async def async_parse_last_reboot(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing last reboot event."""
    topic, payload = util.extract_message(msg)
    return model.EventEntity(
        f"{uid}_{topic}",
        "Last Reboot",
        "sensor",
        "timestamp",
        None,
        payload.Data.SimpleItem[0].Value,
        "diagnostic",
    )


@registry.register("tns1:Monitoring/OperatingTime/LastReset")
async def async_parse_last_reset(uid: str, msg: typing.Any) -> model.EventEntity | None:
    """Handle parsing last reset event."""
    topic, payload = util.extract_message(msg)
    return model.EventEntity(
        f"{uid}_{topic}",
        "Last Reset",
        "sensor",
        "timestamp",
        None,
        payload.Data.SimpleItem[0].Value,
        "diagnostic",
        entity_enabled=False,
    )


@registry.register("tns1:Monitoring/Backup/Last")
async def async_parse_backup_last(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing last backup event."""
    topic, payload = util.extract_message(msg)
    return model.EventEntity(
        f"{uid}_{topic}",
        "Last Backup",
        "sensor",
        "timestamp",
        None,
        payload.Data.SimpleItem[0].Value,
        "diagnostic",
        entity_enabled=False,
    )


@registry.register("tns1:Monitoring/OperatingTime/LastClockSynchronization")
async def async_parse_last_clock_sync(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing last clock synchronization event."""
    topic, payload = util.extract_message(msg)
    return model.EventEntity(
        f"{uid}_{topic}",
        "Last Clock Synchronization",
        "sensor",
        "timestamp",
        None,
        payload.Data.SimpleItem[0].Value,
        "diagnostic",
        entity_enabled=False,
    )


@registry.register("tns1:RecordingConfig/JobState")
async def async_parse_jobstate(uid: str, msg: typing.Any) -> model.EventEntity | None:
    """Handle parsing recording job state event."""
    topic, payload = util.extract_message(msg)
    source = payload.Source.SimpleItem[0].Value
    return model.EventEntity(
        f"{uid}_{topic}_{source}",
        "Recording Job State",
        "binary_sensor",
        None,
        None,
        payload.Data.SimpleItem[0].Value == "Active",
        "diagnostic",
    )


@registry.register("tns1:RuleEngine/LineDetector/Crossed")
async def async_parse_linedetector_crossed(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing line detector crossed event."""
    video_source = ""
    video_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = source.Value
        if source.Name == "VideoAnalyticsConfigurationToken":
            video_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}_{video_analytics}_{rule}",
        "Line Detector Crossed",
        "sensor",
        None,
        None,
        payload.Data.SimpleItem[0].Value,
        "diagnostic",
    )


@registry.register("tns1:RuleEngine/CountAggregation/Counter")
async def async_parse_count_aggregation_counter(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing count aggregation counter event."""
    video_source = ""
    video_analytics = ""
    rule = ""
    topic, payload = util.extract_message(msg)
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = util.normalize_video_source(source.Value)
        if source.Name == "VideoAnalyticsConfigurationToken":
            video_analytics = source.Value
        if source.Name == "Rule":
            rule = source.Value

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}_{video_analytics}_{rule}",
        "Count Aggregation Counter",
        "sensor",
        None,
        None,
        payload.Data.SimpleItem[0].Value,
        "diagnostic",
    )


@registry.register("tns1:UserAlarm/IVA/HumanShapeDetect")
async def async_parse_human_shape_detect(
    uid: str, msg: typing.Any
) -> model.EventEntity | None:
    """Handle parsing human shape detect event."""
    topic, payload = util.extract_message(msg)
    video_source = ""
    for source in payload.Source.SimpleItem:
        if source.Name == "VideoSourceConfigurationToken":
            video_source = util.normalize_video_source(source.Value)
            break

    return model.EventEntity(
        f"{uid}_{topic}_{video_source}",
        "Human Shape Detect",
        "binary_sensor",
        "motion",
        None,
        payload.Data.SimpleItem[0].Value == "true",
    )
