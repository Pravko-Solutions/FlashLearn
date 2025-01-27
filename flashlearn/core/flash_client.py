import litellm

class FlashLiteLLMClient:
    def __init__(self):
        pass

    class Chat:
        # Define the Completions class inside Chat
        class Completions:
            @staticmethod
            def create(**kwargs):
                # This function passes kwargs to litellm's completion method
                # Replace 'litellm.completion' with the actual function path if incorrect
                kwargs.update({'no-log': True})
                return litellm.completion(**kwargs)

        # Expose completions as a property of Chat
        @property
        def completions(self):
            return self.Completions()

    # Create an instance of Chat as a class attribute
    chat = Chat()

