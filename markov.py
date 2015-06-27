#!/usr/bin/env python
import re
import json

probs = { }

def main():
	source_text = """
	Undoubtedly, much of this national mood of hostility to government and business came out of the Vietnam war: its moral shame, its exposure of government lies and atrocities. On top of this came the political disgrace of the Nixon administration in the scandals that came to be known by the one-word label "Watergate," and which led to the historic resignation from the presidency, the first in American history of Richard Nixon in August 1974. The Draco reptoids, usually standing seven to twelve feet tall, have been reported to be the royal elitists of the reptoid hierarchy. They are seen far less often than other reptoids types. The Draco are similar in appearance to the Reptoid, but they have distinct physical differences. Why did Carl Jung, Moses, the Freemasons, the Baptists and so many other groups of people throughout history looked upon the image of a serpent and, through handling the image without fear, represented it as a symbol of our unquestioned love for God and our divine spirituality. Why are dreams of snakes, dragons, lizards or other reptilian animals seem so real and provocative at times?

For almost 200 years, the policy of this Nation has been made under our Constitution by those leaders in the Congress and the White House elected by all of the people. If a vocal minority, however fervent its cause, prevails over reason and the will of the majority, this Nation has no future as a free society.
And now I would like to address a word, if I may, to the young people of this Nation who are particularly concerned, and I understand why they are concerned, about this war. The answer to these questions may be found in the fact that, according to evolutionary science, reptiles were at the root of a genetic matrix from which all land vertebrate life evolved. Millions of years of biological divergence from the trunk of the vertebrate "Tree of Life" resulted in a world full of back boned animals that, despite their dissimilar outward appearance, share the same parental lineage---an encoded past locked in their DNA.  A code which we humans share with other land vertebrate life forms.
	"""
	# fix punctuation
	sentence_delimiters = ["...", ".", ";", "?", "!", "---", "--"]
	text_buffer = source_text
	for char in sentence_delimiters:
		text_buffer = text_buffer.replace(char, char+" ")
	# strip useless characters
	useless = ["\t", "\n", "\"", "\'"]
	for char in useless:
		text_buffer = text_buffer.replace(char, "")
	# build probability table
	last_word = " "
	for word in text_buffer.split(" "):
		if not last_word in probs.keys():
			probs[last_word] = {}
			probs[last_word][word] = 1
		else:
			if word not in probs[last_word].keys():
				probs[last_word][word] = 1
			else:
				probs[last_word][word] += 1
		last_word = word
	words_beginning_sentences = "TODO"
	# sample the table
	print json.dumps(probs)

if __name__ == "__main__":
	main()

# http://stackoverflow.com/questions/16720541/python-string-replace-regular-expression
# line = re.sub(r"(?i)^.*interfaceOpDataFile.*$", "interfaceOpDataFile %s" % fileIn, line)