import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Eat more raspberry pie"

        handler_input.response_builder.speak(speech_text).set_should_end_session(
            True)
        return handler_input.response_builder.response


class SetFanSettingsIntentHandler(AbstractRequestHandler):
    """Handler for set_fan_settings Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("set_fan_settings")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Do something here with IR blaster
        power_mode = get_slot_value(handler_input=handler_input, slot_name="power_mode")
        temp_mode = get_slot_value(handler_input=handler_input, slot_name="temp_mode")
        fan_num = get_slot_value(handler_input=handler_input, slot_name="fan_num")
        degrees = get_slot_value(handler_input=handler_input, slot_name="degrees")

        if power_mode:
            handler_input.response_builder.speak(f'Power was toggled to {power_mode}')
        if temp_mode:
            handler_input.response_builder.speak(f'Temp mode was toggled to {temp_mode}')
        if fan_num:
            handler_input.response_builder.speak(f'Fan number was toggled to {fan_num}')
        if degrees:
            handler_input.response_builder.speak(f'Fan was toggled to {degrees} degrees')

        speech_text = "Ending set fan settings intent handling"

        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can ask me to change the settings on your Dyson fan"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Okay"

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is available in these locales.
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "This is an Alexa voice skill for adjusting Dyson fan settings"
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

# Set the skill id, this ensures that this request came from your skill
sb.skill_id = "amzn1.ask.skill.e033e61a-290c-46cf-b4cb-679d9ec858a4"

# Add all request handlers to the skill
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SetFanSettingsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
