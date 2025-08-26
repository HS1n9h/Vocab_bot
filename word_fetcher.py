#!/usr/bin/env python3
"""
Word fetching module for Daily Vocabulary Bot.
Handles API calls to dictionary services and provides fallback word lists.
"""

import requests
import logging
import random
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class WordFetcher:
    """Fetches vocabulary words from API or fallback sources."""
    
    def __init__(self):
        """Initialize the word fetcher."""
        self.api_base_url = Config.DICTIONARY_API_URL.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = Config.API_TIMEOUT
        
        # Fallback words when API is unavailable
        self.fallback_words = [
            {
                'word': 'serendipity',
                'meaning': 'Finding something nice when you weren\'t looking for it',
                'part_of_speech': 'noun',
                'example': 'It was serendipity when I found my favorite toy under the bed!'
            },
            {
                'word': 'ephemeral',
                'meaning': 'Something that doesn\'t last very long',
                'part_of_speech': 'adjective',
                'example': 'Rainbows are ephemeral - they disappear quickly!'
            },
            {
                'word': 'ubiquitous',
                'meaning': 'Something that is everywhere you look',
                'part_of_speech': 'adjective',
                'example': 'Cars are ubiquitous in the city - you see them everywhere!'
            },
            {
                'word': 'eloquent',
                'meaning': 'Speaking in a beautiful and clear way',
                'part_of_speech': 'adjective',
                'example': 'The storyteller was so eloquent that everyone listened quietly.'
            },
            {
                'word': 'resilient',
                'meaning': 'Bouncing back quickly when something bad happens',
                'part_of_speech': 'adjective',
                'example': 'Kids are resilient - they get up and try again when they fall!'
            },
            {
                'word': 'authentic',
                'meaning': 'Real and true, not fake',
                'part_of_speech': 'adjective',
                'example': 'This is an authentic dinosaur bone from millions of years ago!'
            },
            {
                'word': 'innovative',
                'meaning': 'Coming up with new and clever ideas',
                'part_of_speech': 'adjective',
                'example': 'The inventor was innovative - he created a robot that cleans rooms!'
            },
            {
                'word': 'persistent',
                'meaning': 'Not giving up, even when it\'s hard',
                'part_of_speech': 'adjective',
                'example': 'The persistent ant kept carrying food until it reached its home.'
            },
            {
                'word': 'versatile',
                'meaning': 'Able to do many different things',
                'part_of_speech': 'adjective',
                'example': 'A pencil is versatile - you can write, draw, and even use it as a ruler!'
            },
            {
                'word': 'diligent',
                'meaning': 'Working hard and being careful with your work',
                'part_of_speech': 'adjective',
                'example': 'The diligent student finished all her homework before playing.'
            },
            {
                'word': 'magnificent',
                'meaning': 'Very beautiful and impressive',
                'part_of_speech': 'adjective',
                'example': 'The magnificent castle had towers that touched the clouds!'
            },
            {
                'word': 'curious',
                'meaning': 'Wanting to know more about things',
                'part_of_speech': 'adjective',
                'example': 'The curious cat explored every corner of the new house.'
            },
            {
                'word': 'generous',
                'meaning': 'Sharing with others and being kind',
                'part_of_speech': 'adjective',
                'example': 'The generous boy shared his cookies with his friends.'
            },
            {
                'word': 'courageous',
                'meaning': 'Brave and not afraid to do the right thing',
                'part_of_speech': 'adjective',
                'example': 'The courageous firefighter saved the kitten from the tree.'
            },
            {
                'word': 'brilliant',
                'meaning': 'Very smart and clever',
                'part_of_speech': 'adjective',
                'example': 'The brilliant scientist discovered how to make plants grow faster.'
            },
            {
                'word': 'adventurous',
                'meaning': 'Loving to try new things and explore',
                'part_of_speech': 'adjective',
                'example': 'The adventurous explorer climbed the highest mountain.'
            },
            {
                'word': 'compassionate',
                'meaning': 'Caring about others and their feelings',
                'part_of_speech': 'adjective',
                'example': 'The compassionate nurse comforted the scared little patient.'
            },
            {
                'word': 'enthusiastic',
                'meaning': 'Very excited and happy about something',
                'part_of_speech': 'adjective',
                'example': 'The enthusiastic puppy wagged its tail when it saw its owner.'
            },
            {
                'word': 'determined',
                'meaning': 'Having a strong goal and working hard to reach it',
                'part_of_speech': 'adjective',
                'example': 'The determined athlete practiced every day to win the race.'
            },
            {
                'word': 'imaginative',
                'meaning': 'Good at thinking of creative and fun ideas',
                'part_of_speech': 'adjective',
                'example': 'The imaginative artist painted pictures of flying elephants!'
            },
            {
                'word': 'meticulous',
                'meaning': 'Being very careful and paying attention to small details',
                'part_of_speech': 'adjective',
                'example': 'The meticulous builder made sure every brick was perfectly straight.'
            },
            {
                'word': 'optimistic',
                'meaning': 'Always thinking that good things will happen',
                'part_of_speech': 'adjective',
                'example': 'The optimistic girl believed she would find her lost toy.'
            },
            {
                'word': 'tenacious',
                'meaning': 'Holding on tightly and not letting go',
                'part_of_speech': 'adjective',
                'example': 'The tenacious dog held onto its toy and wouldn\'t let go.'
            },
            {
                'word': 'astute',
                'meaning': 'Very smart and good at understanding things quickly',
                'part_of_speech': 'adjective',
                'example': 'The astute detective solved the mystery in just one day.'
            },
            {
                'word': 'charismatic',
                'meaning': 'Having a special charm that makes people like you',
                'part_of_speech': 'adjective',
                'example': 'The charismatic teacher made learning fun for everyone.'
            },
            # Adding more ADVANCED vocabulary words that are actually worth learning
            {
                'word': 'perspicacious',
                'meaning': 'Having a deep understanding and insight into things',
                'part_of_speech': 'adjective',
                'example': 'The perspicacious teacher could see when students were struggling.'
            },
            {
                'word': 'magnanimous',
                'meaning': 'Generous in forgiving others and not holding grudges',
                'part_of_speech': 'adjective',
                'example': 'The magnanimous winner congratulated the other team.'
            },
            {
                'word': 'voracious',
                'meaning': 'Having a huge appetite for something, especially reading',
                'part_of_speech': 'adjective',
                'example': 'The voracious reader finished three books in one week.'
            },
            {
                'word': 'ubiquitous',
                'meaning': 'Present everywhere at the same time',
                'part_of_speech': 'adjective',
                'example': 'Smartphones are ubiquitous in modern society.'
            },
            {
                'word': 'enigmatic',
                'meaning': 'Mysterious and difficult to understand',
                'part_of_speech': 'adjective',
                'example': 'The enigmatic painting left everyone wondering what it meant.'
            },
            {
                'word': 'diligent',
                'meaning': 'Working with careful attention and effort',
                'part_of_speech': 'adjective',
                'example': 'The diligent student studied every night for the exam.'
            },
            {
                'word': 'eloquent',
                'meaning': 'Speaking or writing in a beautiful and expressive way',
                'part_of_speech': 'adjective',
                'example': 'The eloquent speaker moved the entire audience to tears.'
            },
            {
                'word': 'resilient',
                'meaning': 'Able to recover quickly from difficulties',
                'part_of_speech': 'adjective',
                'example': 'The resilient community rebuilt after the storm.'
            },
            {
                'word': 'authentic',
                'meaning': 'Genuine and real, not fake or copied',
                'part_of_speech': 'adjective',
                'example': 'The restaurant served authentic Italian food.'
            },
            {
                'word': 'innovative',
                'meaning': 'Introducing new ideas or methods',
                'part_of_speech': 'adjective',
                'example': 'The innovative company created a revolutionary product.'
            },
            {
                'word': 'persistent',
                'meaning': 'Continuing firmly despite obstacles',
                'part_of_speech': 'adjective',
                'example': 'The persistent inventor tried 100 times before succeeding.'
            },
            {
                'word': 'versatile',
                'meaning': 'Able to adapt to many different uses',
                'part_of_speech': 'adjective',
                'example': 'The versatile tool can be used for many different jobs.'
            },
            {
                'word': 'magnificent',
                'meaning': 'Extremely beautiful and impressive',
                'part_of_speech': 'adjective',
                'example': 'The magnificent palace took 20 years to build.'
            },
            {
                'word': 'curious',
                'meaning': 'Eager to learn or know something',
                'part_of_speech': 'adjective',
                'example': 'The curious scientist asked many questions.'
            },
            {
                'word': 'generous',
                'meaning': 'Willing to give more than is necessary',
                'part_of_speech': 'adjective',
                'example': 'The generous donor gave millions to charity.'
            },
            {
                'word': 'courageous',
                'meaning': 'Brave and willing to face danger',
                'part_of_speech': 'adjective',
                'example': 'The courageous firefighter saved the child from the fire.'
            },
            {
                'word': 'brilliant',
                'meaning': 'Exceptionally intelligent or talented',
                'part_of_speech': 'adjective',
                'example': 'The brilliant mathematician solved the impossible problem.'
            },
            {
                'word': 'adventurous',
                'meaning': 'Willing to take risks and try new things',
                'part_of_speech': 'adjective',
                'example': 'The adventurous explorer discovered ancient ruins.'
            },
            {
                'word': 'compassionate',
                'meaning': 'Feeling sympathy and concern for others',
                'part_of_speech': 'adjective',
                'example': 'The compassionate doctor comforted the worried patient.'
            },
            {
                'word': 'enthusiastic',
                'meaning': 'Showing intense excitement and interest',
                'part_of_speech': 'adjective',
                'example': 'The enthusiastic crowd cheered for their team.'
            },
            {
                'word': 'determined',
                'meaning': 'Having a strong will to achieve something',
                'part_of_speech': 'adjective',
                'example': 'The determined athlete trained for years to win the gold medal.'
            },
            {
                'word': 'imaginative',
                'meaning': 'Creative and full of imagination',
                'part_of_speech': 'adjective',
                'example': 'The imaginative writer created a whole new world in her book.'
            },
            {
                'word': 'meticulous',
                'meaning': 'Very careful and precise about details',
                'part_of_speech': 'adjective',
                'example': 'The meticulous craftsman created perfect furniture.'
            },
            {
                'word': 'optimistic',
                'meaning': 'Hopeful and confident about the future',
                'part_of_speech': 'adjective',
                'example': 'The optimistic leader inspired hope during challenging times.'
            },
            {
                'word': 'tenacious',
                'meaning': 'Persistent and not giving up easily',
                'part_of_speech': 'adjective',
                'example': 'The tenacious lawyer fought for justice for many years.'
            },
            {
                'word': 'astute',
                'meaning': 'Clever and good at understanding situations',
                'part_of_speech': 'adjective',
                'example': 'The astute investor made profitable decisions.'
            },
            {
                'word': 'charismatic',
                'meaning': 'Having a compelling charm that inspires devotion',
                'part_of_speech': 'adjective',
                'example': 'The charismatic teacher made learning exciting for everyone.'
            },
            {
                'word': 'sagacious',
                'meaning': 'Wise and showing good judgment',
                'part_of_speech': 'adjective',
                'example': 'The sagacious elder gave wise advice to the young people.'
            },
            {
                'word': 'prudent',
                'meaning': 'Careful and sensible in making decisions',
                'part_of_speech': 'adjective',
                'example': 'The prudent investor saved money for emergencies.'
            },
            {
                'word': 'arduous',
                'meaning': 'Requiring great effort and hard work',
                'part_of_speech': 'adjective',
                'example': 'The arduous journey through the mountains took weeks.'
            },
            {
                'word': 'concise',
                'meaning': 'Brief but comprehensive and clear',
                'part_of_speech': 'adjective',
                'example': 'The concise explanation helped everyone understand quickly.'
            },
            {
                'word': 'diligent',
                'meaning': 'Working with steady effort and attention',
                'part_of_speech': 'adjective',
                'example': 'The diligent student completed all assignments on time.'
            },
            {
                'word': 'eloquent',
                'meaning': 'Fluent and persuasive in speech or writing',
                'part_of_speech': 'adjective',
                'example': 'The eloquent speaker moved the entire audience.'
            },
            {
                'word': 'resilient',
                'meaning': 'Able to withstand and recover from difficulties',
                'part_of_speech': 'adjective',
                'example': 'The resilient community rebuilt stronger after the disaster.'
            },
            {
                'word': 'authentic',
                'meaning': 'Genuine and not counterfeit or copied',
                'part_of_speech': 'adjective',
                'example': 'The restaurant served authentic cuisine from the region.'
            },
            {
                'word': 'innovative',
                'meaning': 'Featuring new methods or ideas',
                'part_of_speech': 'adjective',
                'example': 'The innovative company revolutionized the industry.'
            },
            {
                'word': 'persistent',
                'meaning': 'Continuing firmly despite opposition or difficulty',
                'part_of_speech': 'adjective',
                'example': 'The persistent inventor never gave up on his dream.'
            },
            {
                'word': 'versatile',
                'meaning': 'Capable of adapting to many different functions',
                'part_of_speech': 'adjective',
                'example': 'The versatile tool can be used for multiple purposes.'
            },
            {
                'word': 'magnificent',
                'meaning': 'Extremely beautiful and impressive',
                'part_of_speech': 'adjective',
                'example': 'The magnificent cathedral took centuries to complete.'
            },
            {
                'word': 'curious',
                'meaning': 'Eager to learn or know something',
                'part_of_speech': 'adjective',
                'example': 'The curious child asked questions about everything.'
            },
            {
                'word': 'generous',
                'meaning': 'Willing to give more than is necessary',
                'part_of_speech': 'adjective',
                'example': 'The generous donor supported many charitable causes.'
            },
            {
                'word': 'courageous',
                'meaning': 'Brave and willing to face danger or difficulty',
                'part_of_speech': 'adjective',
                'example': 'The courageous soldier protected his comrades.'
            },
            {
                'word': 'brilliant',
                'meaning': 'Exceptionally intelligent or talented',
                'part_of_speech': 'adjective',
                'example': 'The brilliant scientist made groundbreaking discoveries.'
            },
            {
                'word': 'adventurous',
                'meaning': 'Willing to take risks and try new experiences',
                'part_of_speech': 'adjective',
                'example': 'The adventurous traveler explored remote parts of the world.'
            },
            {
                'word': 'compassionate',
                'meaning': 'Feeling sympathy and concern for others',
                'part_of_speech': 'adjective',
                'example': 'The compassionate nurse cared for patients with kindness.'
            },
            {
                'word': 'enthusiastic',
                'meaning': 'Showing intense excitement and interest',
                'part_of_speech': 'adjective',
                'example': 'The enthusiastic fans cheered loudly for their team.'
            },
            {
                'word': 'determined',
                'meaning': 'Having a strong will to achieve something',
                'part_of_speech': 'adjective',
                'example': 'The determined athlete trained for years to reach the Olympics.'
            },
            {
                'word': 'imaginative',
                'meaning': 'Creative and full of imagination',
                'part_of_speech': 'adjective',
                'example': 'The imaginative artist created unique and beautiful paintings.'
            },
            {
                'word': 'meticulous',
                'meaning': 'Very careful and precise about details',
                'part_of_speech': 'adjective',
                'example': 'The meticulous craftsman created perfect furniture.'
            },
            {
                'word': 'optimistic',
                'meaning': 'Hopeful and confident about the future',
                'part_of_speech': 'adjective',
                'example': 'The optimistic leader inspired hope during challenging times.'
            },
            {
                'word': 'tenacious',
                'meaning': 'Persistent and not giving up easily',
                'part_of_speech': 'adjective',
                'example': 'The tenacious lawyer fought for justice for many years.'
            },
            {
                'word': 'astute',
                'meaning': 'Clever and good at understanding situations',
                'part_of_speech': 'adjective',
                'example': 'The astute investor made profitable decisions.'
            },
            {
                'word': 'charismatic',
                'meaning': 'Having a compelling charm that inspires devotion',
                'part_of_speech': 'adjective',
                'example': 'The charismatic teacher made learning exciting for everyone.'
            }
        ]
    
    def fetch_word_from_api(self, word: str) -> Optional[Dict]:
        """Fetch word definition from the Dictionary API."""
        try:
            url = f"{self.api_base_url}/{word.lower()}"
            logger.info(f"Fetching word from API: {word}")
            
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            if not data or not isinstance(data, list):
                logger.warning(f"Invalid API response for word: {word}")
                return None
            
            word_data = data[0]
            meanings = word_data.get('meanings', [])
            
            if not meanings:
                logger.warning(f"No meanings found for word: {word}")
                return None
            
            # Get the first meaning
            meaning = meanings[0]
            definitions = meaning.get('definitions', [])
            
            if not definitions:
                logger.warning(f"No definitions found for word: {word}")
                return None
            
            definition = definitions[0].get('definition', 'No definition available')
            part_of_speech = meaning.get('partOfSpeech', 'unknown')
            
            # Get example sentence
            examples = meaning.get('definitions', [])
            example = None
            for def_item in examples:
                if 'example' in def_item:
                    example = def_item['example']
                    break
            
            return {
                'word': word.lower(),
                'meaning': self.simplify_definition(definition),
                'part_of_speech': part_of_speech,
                'example': self.create_kid_friendly_example(word, definition)  # Always use our good examples
            }
            
        except requests.RequestException as e:
            logger.error(f"API request failed for word '{word}': {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing API response for word '{word}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching word '{word}': {e}")
            return None
    
    def get_random_words(self, count: int, exclude_words: List[str] = None) -> List[Dict]:
        """Get random words from the fallback list, excluding already sent words."""
        if exclude_words is None:
            exclude_words = []
        
        # Filter out already sent words
        available_words = [
            word for word in self.fallback_words 
            if word['word'].lower() not in [w.lower() for w in exclude_words]
        ]
        
        if not available_words:
            logger.warning("No available words in fallback list")
            return []
        
        # Shuffle and return requested number of words
        random.shuffle(available_words)
        return available_words[:min(count, len(available_words))]
    
    def get_new_words(self, count: int, exclude_words: List[str] = None) -> List[Dict]:
        """Get new words, trying API first, then falling back to local list."""
        if exclude_words is None:
            exclude_words = []
        
        new_words = []
        attempts = 0
        max_attempts = count * 3  # Try more words than needed to account for duplicates
        
        # Try to get words from API first
        while len(new_words) < count and attempts < max_attempts:
            attempts += 1
            
            # Try a random word from fallback list
            random_word = random.choice(self.fallback_words)
            word_text = random_word['word']
            
            # Skip if already in our list or excluded
            if (word_text.lower() in [w['word'].lower() for w in new_words] or
                word_text.lower() in exclude_words):
                continue
            
            # Try API first, but prefer our fallback definitions for better quality
            api_word = self.fetch_word_from_api(word_text)
            if api_word:
                # Check if the API definition is too complex
                if self._is_too_complex(api_word['meaning']):
                    # Use our better fallback definition instead
                    new_words.append(random_word)
                    logger.info(f"API definition too complex, using fallback: {word_text}")
                else:
                    # Even if not too complex, check if our fallback is better
                    if self._is_fallback_better(random_word['meaning'], api_word['meaning']):
                        new_words.append(random_word)
                        logger.info(f"Our fallback definition is better, using it: {word_text}")
                    else:
                        new_words.append(api_word)
                        logger.info(f"Using API definition: {word_text}")
            else:
                # Fall back to local definition
                new_words.append(random_word)
                logger.info(f"Using fallback word: {word_text}")
        
        # If we still don't have enough words, add more from fallback
        if len(new_words) < count:
            additional_words = self.get_random_words(
                count - len(new_words), 
                [w['word'] for w in new_words] + exclude_words
            )
            new_words.extend(additional_words)
        
        logger.info(f"Retrieved {len(new_words)} new words")
        return new_words[:count]
    
    def test_api_connection(self) -> bool:
        """Test if the Dictionary API is accessible."""
        try:
            test_word = 'test'
            url = f"{self.api_base_url}/{test_word}"
            response = self.session.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"API connection test failed: {e}")
            return False
    
    def get_fallback_word_count(self) -> int:
        """Get the number of available fallback words."""
        return len(self.fallback_words)

    def simplify_definition(self, definition: str) -> str:
        """Simplify complex definitions to make them kid-friendly."""
        # First, detect and fix circular definitions
        if self._is_circular_definition(definition):
            return self._get_better_definition(definition)
        
        # Replace complex words with simpler ones
        replacements = {
            'the occurrence and development of events by chance in a happy or beneficial way': 'finding something nice when you weren\'t looking for it',
            'lasting for a very short time': 'something that doesn\'t last very long',
            'transitory': 'temporary',
            'present, appearing, or found everywhere': 'something that is everywhere you look',
            'fluent or persuasive in speaking or writing': 'speaking in a beautiful and clear way',
            'able to withstand or recover quickly from difficult conditions': 'bouncing back quickly when something bad happens',
            'genuine or real; not false or copied': 'real and true, not fake',
            'featuring new methods, advanced ideas, or creative thinking': 'coming up with new and clever ideas',
            'continuing firmly or obstinately in a course of action': 'not giving up, even when it\'s hard',
            'able to adapt or be adapted to many different functions or activities': 'able to do many different things',
            'having or showing care and conscientiousness in one\'s work or duties': 'working hard and being careful with your work',
            'very beautiful and impressive': 'very beautiful and impressive',
            'wanting to know more about things': 'wanting to know more about things',
            'sharing with others and being kind': 'sharing with others and being kind',
            'brave and not afraid to do the right thing': 'brave and not afraid to do the right thing',
            'very smart and clever': 'very smart and clever',
            'loving to try new things and explore': 'loving to try new things and explore',
            'caring about others and their feelings': 'caring about others and their feelings',
            'very excited and happy about something': 'very excited and happy about something',
            'having a strong goal and working hard to reach it': 'having a strong goal and working hard to reach it',
            'good at thinking of creative and fun ideas': 'good at thinking of creative and fun ideas'
        }
        
        # Check if we have a direct replacement
        for complex_def, simple_def in replacements.items():
            if complex_def.lower() in definition.lower():
                return simple_def
        
        # General simplification rules
        simplified = definition
        
        # Remove complex phrases and replace with simple ones
        complex_phrases = [
            'the occurrence and development of',
            'by chance in a happy or beneficial way',
            'able to withstand or recover quickly from',
            'featuring new methods, advanced ideas, or',
            'continuing firmly or obstinately in',
            'having or showing care and conscientiousness in',
            'able to adapt or be adapted to many different functions or activities',
            'to feel compassion',
            'with regard to something',
            'to regard someone or something with'
        ]
        
        for phrase in complex_phrases:
            if phrase.lower() in simplified.lower():
                # Try to extract the core meaning
                if 'serendipity' in definition.lower():
                    simplified = 'Finding something nice when you weren\'t looking for it'
                elif 'ephemeral' in definition.lower():
                    simplified = 'Something that doesn\'t last very long'
                elif 'ubiquitous' in definition.lower():
                    simplified = 'Something that is everywhere you look'
                elif 'eloquent' in definition.lower():
                    simplified = 'Speaking in a beautiful and clear way'
                elif 'resilient' in definition.lower():
                    simplified = 'Bouncing back quickly when something bad happens'
                elif 'authentic' in definition.lower():
                    simplified = 'Real and true, not fake'
                elif 'innovative' in definition.lower():
                    simplified = 'Coming up with new and clever ideas'
                elif 'persistent' in definition.lower():
                    simplified = 'Not giving up, even when it\'s hard'
                elif 'versatile' in definition.lower():
                    simplified = 'Able to do many different things'
                elif 'diligent' in definition.lower():
                    simplified = 'Working hard and being careful with your work'
                elif 'compassionate' in definition.lower():
                    simplified = 'Caring about others and their feelings'
                break
        
        return simplified

    def _is_circular_definition(self, definition: str) -> bool:
        """Check if a definition is circular (defines a word with itself)."""
        # Common circular definition patterns
        circular_patterns = [
            'to feel compassion',
            'with compassion',
            'having compassion',
            'showing compassion',
            'regard with compassion',
            'feeling compassion',
            'compassion for',
            'compassion with'
        ]
        
        for pattern in circular_patterns:
            if pattern.lower() in definition.lower():
                return True
        
        return False

    def _get_better_definition(self, bad_definition: str) -> str:
        """Get a much better definition when the original is terrible."""
        # Map terrible definitions to good ones
        better_definitions = {
            'compassionate': 'Caring about others and their feelings',
            'serendipity': 'Finding something nice when you weren\'t looking for it',
            'ephemeral': 'Something that doesn\'t last very long',
            'ubiquitous': 'Something that is everywhere you look',
            'eloquent': 'Speaking in a beautiful and clear way',
            'resilient': 'Bouncing back quickly when something bad happens',
            'authentic': 'Real and true, not fake',
            'innovative': 'Coming up with new and clever ideas',
            'persistent': 'Not giving up, even when it\'s hard',
            'versatile': 'Able to do many different things',
            'diligent': 'Working hard and being careful with your work',
            'magnificent': 'Very beautiful and impressive',
            'curious': 'Wanting to know more about things',
            'generous': 'Sharing with others and being kind',
            'courageous': 'Brave and not afraid to do the right thing',
            'brilliant': 'Very smart and clever',
            'adventurous': 'Loving to try new things and explore',
            'enthusiastic': 'Very excited and happy about something',
            'determined': 'Having a strong goal and working hard to reach it',
            'imaginative': 'Good at thinking of creative and fun ideas'
        }
        
        # Try to find the word in the bad definition
        for word, good_def in better_definitions.items():
            if word.lower() in bad_definition.lower():
                return good_def
        
        # If we can't find a specific word, return a generic good definition
        return 'Having a special quality that makes something good or interesting'

    def create_kid_friendly_example(self, word: str, meaning: str) -> str:
        """Create a kid-friendly example sentence for a word."""
        # Create fun, relevant examples for kids
        examples = {
            'serendipity': 'It was serendipity when I found my favorite toy under the bed!',
            'ephemeral': 'Rainbows are ephemeral - they disappear quickly!',
            'ubiquitous': 'Cars are ubiquitous in the city - you see them everywhere!',
            'eloquent': 'The storyteller was so eloquent that everyone listened quietly.',
            'resilient': 'Kids are resilient - they get up and try again when they fall!',
            'authentic': 'This is an authentic dinosaur bone from millions of years ago!',
            'innovative': 'The inventor was innovative - he created a robot that cleans rooms!',
            'persistent': 'The persistent ant kept carrying food until it reached its home.',
            'versatile': 'A pencil is versatile - you can write, draw, and even use it as a ruler!',
            'diligent': 'The diligent student finished all her homework before playing.',
            'magnificent': 'The magnificent castle had towers that touched the clouds!',
            'curious': 'The curious cat explored every corner of the new house.',
            'generous': 'The generous boy shared his cookies with his friends.',
            'courageous': 'The courageous firefighter saved the kitten from the tree.',
            'brilliant': 'The brilliant scientist discovered how to make plants grow faster.',
            'adventurous': 'The adventurous explorer climbed the highest mountain.',
            'compassionate': 'The compassionate nurse comforted the scared little patient.',
            'enthusiastic': 'The enthusiastic puppy wagged its tail when it saw its owner.',
            'determined': 'The determined athlete practiced every day to win the race.',
            'imaginative': 'The imaginative artist painted pictures of flying elephants!',
            'meticulous': 'The meticulous builder made sure every brick was perfectly straight.',
            'optimistic': 'The optimistic girl believed she would find her lost toy.',
            'tenacious': 'The tenacious dog held onto its toy and wouldn\'t let go.',
            'eloquent': 'The eloquent storyteller made everyone listen quietly.',
            'astute': 'The astute detective solved the mystery in just one day.',
            'charismatic': 'The charismatic teacher made learning fun for everyone.',
            'diligent': 'The diligent student finished all her homework before playing.',
            'enthusiastic': 'The enthusiastic puppy wagged its tail when it saw its owner.',
            'persistent': 'The persistent ant kept carrying food until it reached its home.'
        }
        
        # Return the specific example if we have one, otherwise create a generic one
        if word.lower() in examples:
            return examples[word.lower()]
        else:
            # Create a generic kid-friendly example
            return f'The word "{word}" means {meaning.lower()}. Can you use it in a sentence?'

    def _is_too_complex(self, definition: str) -> bool:
        """Check if a definition is too complex for kids."""
        # Words that make definitions too complex for kids
        complex_words = [
            'obstinately', 'refusing', 'inquisitive', 'connotation', 'nosy', 'prying',
            'tending', 'investigate', 'withstand', 'recover', 'difficult', 'conditions',
            'conscientiousness', 'adapt', 'adapted', 'functions', 'activities',
            'occurrence', 'development', 'beneficial', 'transitory', 'persuasive',
            'genuine', 'methods', 'advanced', 'creative', 'firmly', 'course', 'action'
        ]
        
        # Check if definition contains complex words
        for word in complex_words:
            if word.lower() in definition.lower():
                return True
        
        # Check if definition is too long (more than 50 characters)
        if len(definition) > 50:
            return True
        
        # Check if definition has multiple meanings separated by semicolons
        if ';' in definition:
            return True
        
        return False

    def _is_fallback_better(self, fallback_meaning: str, api_meaning: str) -> bool:
        """Check if our fallback definition is better than the API one."""
        # Our fallback definitions are always better for kids
        # They are shorter, simpler, and more appropriate
        return True
