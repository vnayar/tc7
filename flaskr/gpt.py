import openai
from openai.api_resources.completion import Completion
from openai.api_resources.image import Image
from flask.config import Config

"""Manages a connection to OpenAI's GPT and issues text prediction prompts."""
class GptService:
    """If set, use hard-coded test data instead of calling GPT."""
    use_test_data: bool = False

    def __init__(self, config : Config) -> None:
        if 'OPENAI_API_KEY' not in config:
            raise Exception('Missing value for OPENAPI_API_KEY in "instance/openai-config.json"!'
                            '\nSee README.md for details.')
        # Unfortunately this must be configured as a global variable, so each instance of GptQuery
        # can overwrite what the previous one does.
        # Configure OpenAI
        openai.api_key = config['OPENAI_API_KEY']

        self.use_test_data = config.get('OPENAI_TEST_DATA', False)

    """
    Create a GPT prompt to request slides for a pitch deck.

    Params:
      name = The name of the company.
      vision = A 1-sentence description of the company's purpose.
      problem = A brief description of the current unsolved problem people face.
      solution = A brief description of how the company will solve this problem.
      advantage = The competitive advantage that the company has to solve this problem.
      market = A brief description of the size / nature of the customer market.
      team = A listing of the people behind the company.
    """
    def buildPitchDeckPrompt(self,
            name: str, vision: str, problem: str, solution: str,
            advantage: str = '', market: str = '', team: str = '') -> str:
        myPrompt = """
        My business, "{}", has the following vision: <| {} |>

        Customers have a problem: <| {} |>

        My business solves this problem by: <| {} |>

        """.format(
            name,
            vision,
            problem,
            solution)

        if advantage:
            myPrompt += """
            Our business has the following competitive advantages: <| {} |>
            """.format(advantage)

        if market:
            myPrompt += """
            The following is known about the business market: <| {} |>

            """.format(market)

        if team:
            myPrompt += """
            The team behind the business is: <| {} |>

            """.format(team)

        myPrompt += """
        Create a pitch deck for my business to be presented to investors.

        The pitch deck should have slides for the: problem, solution, market, product, business
        model, competitive advantages, team, and business model.

        Each slide should be in the following format:
        
        Slide 1: Slide Title
        - A relevant point.
        - Additional points...

        """
        return myPrompt

    """Submits a prompt to GPT and returns a completion response."""
    def createCompletion(self, prompt: str) -> Completion:
        if self.use_test_data:
            # Use a fake OpenAPI response to save credits during development.
            return type('Completion', (object,), {
	        "choices": [
	            type('Choice', (object,), {
	                "text": """
	                    Slide 1: Ham on Rye
	                    - I Like Ham.
	                    - Ham is good.
	                    Slide 2: Ham on Ham
	                    - Bacon is also good.
	                    - Are fish bacon?
	                    Slide 3: Rye on Ham
	                    - Are you a fish?
	                    - Can fish eat bread?
	                    """
	            })
	        ]
	    })
        else:
            # Using our prompt, call OpenAI to get a probable word completion (an answer).
            return openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                # temperature ranges from 0 (only high probability words) to 1 (lots of randomness)
                temperature=0.4
            )

    
    """Uses the OpenAI API to generate an image representing a given prompt."""
    def createImage(self, prompt: str) -> Image:
        image = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="url",
        )
        print("Received image: ")
        print(image)
        return image
