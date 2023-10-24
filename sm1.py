from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

text_str = '''Finance Minister Nirmala Sitharaman in the Lok Sabha on Thursday. (PTI) Finance Minister Nirmala Sitharaman in the Lok Sabha on Thursday. (PTI)Parliament on Thursday approved changes in the Insolvency and Bankruptcy Code (IBC), providing greater clarity over the distribution of proceeds of the auction of loan defaulting companies, with the Lok Sabha passing the Bill with voice vote. Seven sections of the code are being amended.
The Bill was passed by Rajya Sabha on Monday.The Insolvency and Bankruptcy Code (Amendment) Bill, 2019, gives the committee of creditors of a loan defaulting company explicit authority over the distribution of proceeds in the resolution process, and fixes a firm timeline of 330 days for resolving cases referred to the IBC.The amendments would also bring in more clarity on various provisions, including the time-bound disposal for resolution plan at the application stage, as well as the treatment of financial creditors, Finance Minister Nirmala Sitharaman said.“Once the Corporate Insolvency Resolution Process (CIRP) begins, it has to be completed in 330 days, including litigation stages and judicial process,” Sitharaman said, citing the proposed amendments.The approved resolution plan would be binding on Central and state governments as well as various statutory authorities.Sitharaman said the proposed amendments also respond to issues pertaining to financial creditors in the wake of a recent ruling with respect to financial and operational creditors.
Recently, the National Company Law Appellate Tribunal (NCLAT) had ruled in the Essar Steel Ltd’s case that the Committee of Creditors (CoC) had no role in the distribution of claims, and brought lenders (financial creditors) and vendors (operational creditors) on par.Sitharaman quoted a Supreme Court judgment to say that there is no longer a “defaulter’s paradise” with implementation of the code. She also said the provisions of the Bill empower home buyers. “The government will endeavour to do full justice to them,” she said, adding that the government was also looking at ways to resolve the issue concerning buyers of flats from JP Group of companies.
On issues concerning Jet Airways, the minister said that the stakeholders were free to work out a resolution plan and they were not obliged to use the IBC, which is optional.Earlier, participating in the debate, Gaurav Gogoi of the Congress said the performance of the IBC has been a mixed bag.
 He also raised concerns about the liquidation of companies, especially firms in the real estate sector, that put home buyers’ life savings at risk.M Srinivasulu Reddy of the YSRCP referred to the death of Cafe Coffee Day founder V G Siddhartha and said industries are sick because of business failures. 
 “The government is working towards ‘ease of doing business’, whereas there is an increase in ‘difficulties in doing business’,” he said.
 📣 The Indian Express is now on Telegram. Click here to join our channel (@indianexpress) and stay updated with the latest headlinesFor all the latest India News, download Indian Express App.'''



def _create_frequency_table(text_string) -> dict:
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.
    Removing stop words and making frequency table
    Stemmer - an algorithm to bring words to its root word.
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
    """
    score a sentence by its words
    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        if sentence[:10] in sentenceValue:
            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words

        '''
        Notice that a potential issue with our score algorithm is that long sentences will have an advantage over short sentences. 
        To solve this, we're dividing every sentence score by the number of words in the sentence.
        
        Note that here sentence[:10] is the first 10 character of any sentence, this is to save memory while saving keys of
        the dictionary.
        '''

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


def run_summarization(text):
    # 1 Create the word frequency table
    freq_table = _create_frequency_table(text)

    '''
    We already have a sentence tokenizer, so we just need 
    to run the sent_tokenize() method to create the array of sentences.
    '''

    # 2 Tokenize the sentences
    sentences = sent_tokenize(text)

    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)

    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)

    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.5 * threshold)

    return summary


if __name__ == '__main__':
    #text_str.replace("'","$")
    #text_str.replace('"','%')
    
    result = run_summarization(text_str)
    print(result)