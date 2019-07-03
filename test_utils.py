import unittest
from utils import *


class TestUtils(unittest.TestCase):

    def test_validate_str(self):
        self.assertRaises(ValueError, lambda: validate_str(2))
        self.assertRaises(ValueError, lambda: validate_str(2.5))
        self.assertRaises(ValueError, lambda: validate_str(False))
        self.assertRaises(ValueError, lambda: validate_str(None))
        validate_str('lingo')

    def test_validate_str_list(self):
        self.assertRaises(ValueError, lambda: validate_str_list(2))
        self.assertRaises(ValueError, lambda: validate_str_list(2.5))
        self.assertRaises(ValueError, lambda: validate_str_list(False))
        self.assertRaises(ValueError, lambda: validate_str_list(None))
        self.assertRaises(ValueError, lambda: validate_str_list(['a', 'b', None]))
        validate_str_list(['a', 'b', 'c'])

    def test_has_invalid_characters(self):
        self.assertTrue(has_invalid_characters('gh0st'))
        self.assertTrue(has_invalid_characters('compound word'))
        self.assertTrue(has_invalid_characters('compound-word'))
        self.assertTrue(has_invalid_characters("apostrophe'"))
        self.assertFalse(has_invalid_characters('espousal'))


    def test_too_similar(self):
        self.assertFalse(too_similar(None, 25.2))
        self.assertFalse(too_similar('string', 25))
        self.assertFalse(too_similar(list(), 'beans'))
        self.assertFalse(too_similar('self', 'other'))
        self.assertTrue(too_similar('dog', 'dog'))
        self.assertTrue(too_similar('dog', 'dogs'))
        self.assertTrue(too_similar('dogs', 'dog'))

    def test_filter_word(self):
        self.assertFalse(filter_word('an'))
        self.assertFalse(filter_word('nonexistentword'))
        self.assertFalse(filter_word('errantry'))  # 1.51e-08 so below threshold
        self.assertTrue(filter_word('crepuscular'))  # 7.41e-08 so OK
        self.assertTrue(filter_word('puppy'))

    def test_filter_word_list_quick(self):
        word_list = ['the', 'crepuscular', 'dogs']
        self.assertEqual(filter_word_list_quick(word_list), word_list) ## All spelled correctly
        word_list = ['the', 'underworld', 'gh0st', 'errantry', 'an']
        valid_words = ['the', 'underworld']
        self.assertEqual(filter_word_list_quick(word_list), valid_words)

    def test_filter_word_list_spellcheck(self):
        word_list = ['araignment', 'arraignment', 'dynosaur', 'dinosaur']
        correctly_spelled_word_list = ['arraignment', 'dinosaur']
        self.assertEqual(filter_word_list_quick(word_list), correctly_spelled_word_list)

    def test_rhymes(self):
        self.assertEqual(rhymes('metamorphosis'), [])
        results = rhymes('clouds')
        self.assertEqual(sorted(results), ['crowds', 'shrouds'])

        expected_rhyme_list = ['doubting', 'flouting', 'grouting', 'outing', 'pouting', 'rerouting', 'routing',
                           'scouting', 'shouting', 'spouting', 'touting']
        results = rhymes('sprouting')
        self.assertNotIn('sprouting', results)
        self.assertEqual(sorted(results), expected_rhyme_list)

        results = rhymes('sprouting', sample_size=6)
        self.assertEqual(len(results), 6)
        self.assertTrue(set(expected_rhyme_list).issuperset(set(results)))

    def test_rhyme(self):
        self.assertIsNone(rhyme('metamorphosis'))
        self.assertIn(rhyme('sprouting'), rhymes('sprouting'))

    def test_similar_sounding_words(self):
        all_similar_sounding_words = ['hastening', 'heightening', 'hominid', 'hominy', 'homonym', 'homonyms',
                                      'summoning', 'synonym']
        self.assertEqual(sorted(similar_sounding_words('homonym', sample_size=None)), all_similar_sounding_words)
        results = similar_sounding_words('homonym')
        self.assertEqual(len(results), 6)
        self.assertTrue(set(all_similar_sounding_words).issuperset(set(results)))
        pass

    def test_similar_sounding_word(self):
        self.assertIsNone(rhyme('metamorphosis'))
        all_similar_sounding_words = ['hastening', 'heightening', 'hominid', 'hominy', 'homonym', 'homonyms',
                                      'summoning', 'synonym']  # Using this to save API call in test
        self.assertIn(similar_sounding_word('homonym'), all_similar_sounding_words)

    def test_phonetically_related_words(self):
        self.assertRaises(ValueError, lambda: phonetically_related_words(2))
        self.assertRaises(ValueError, lambda: phonetically_related_words(2.5))
        self.assertRaises(ValueError, lambda: phonetically_related_words(False))
        self.assertRaises(ValueError, lambda: phonetically_related_words(None))
        self.assertRaises(ValueError, lambda: phonetically_related_words(['a', 'b', None]))
        expected_pr_words = ['inchoate', 'payout', 'pet', 'peyote', 'pit', 'poached', 'poet', 'poets', 'poked',
                             'post', 'putt']  # for input 'poet'
        self.assertEqual(sorted(phonetically_related_words('poet', sample_size=None)), expected_pr_words)
        results = phonetically_related_words('poet', sample_size=5)
        self.assertEqual(len(sorted(results)), 5)
        self.assertTrue(set(sorted(expected_pr_words)).issuperset(set(results)))
        expected_pr_words = sorted(expected_pr_words + ['eon', 'gnawing', 'kneeing', 'naan', 'neon', 'non', 'noun'])
        self.assertEqual(sorted(phonetically_related_words(['poet', 'neon'], sample_size=None)), expected_pr_words)

    def test_poem_line_from_word_list(self):
        input_word_list = ['crypt', 'crypts', 'crypt', 'ghost', 'ghosts', 'lost', 'time', 'times']
        possible_connectors = [',', '...', '&', 'and', 'or', '->']
        possible_line_enders = ['.', ',', '!', '?', '...']
        pr_words = phonetically_related_words(input_word_list)
        possible_words = pr_words.copy()
        for line_ender in line_enders:
            for word in pr_words:
                # Since we are testing using .split(), the list of possible words should include f'{word + line ender}'
                possible_words.append(word + line_ender)
        for i in range(3):
            poem_line = poem_line_from_word_list(input_word_list)
            # First character of line should not be a space as indents are handled by the poem_from_word_list function
            self.assertNotEqual(poem_line[0], ' ')
            # Should not have newlines as these are handled by the poem_from_word_list function
            self.assertNotIn('\n', poem_line)
            # When split, everything should derive from the possible word list
            self.assertTrue(set(possible_words + possible_connectors).issuperset(set(poem_line.split())))
            word, last_word = None, None
            for i in range(len(poem_line.split())):
                word = re.match(r'[a-zA-Z]*', '...').group()
                #  No word should be too similar to the preceding word
                self.assertFalse(too_similar(word, last_word))
                last_word = word

    def test_poem_from_word_list(self):
        pass


if __name__ == '__main__':
    unittest.main()