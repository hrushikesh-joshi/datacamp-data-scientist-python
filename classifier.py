import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import punkt
from nltk.corpus.reader import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

path_models = "/Users/Jatin_6700/Downloads/Latest-News-Classifier-master/0. Latest News Classifier/04. Model Training/Models/"
# SVM
path_svm = path_models + 'best_svc.pickle'
with open(path_svm, 'rb') as data:
    svc_model = pickle.load(data)
path_tfidf = "/Users/Jatin_6700/Downloads/Latest-News-Classifier-master/0. Latest News Classifier/03. Feature Engineering/Pickles/tfidf.pickle"
with open(path_tfidf, 'rb') as data:
    tfidf = pickle.load(data)

category_codes = {
    'Business': 0,
    'Entertainment': 1,
    'Politics': 2,
    'Sport': 3,
    'Technology': 4
}
punctuation_signs = list("?:!.,;")
stop_words = list(stopwords.words('english'))

def create_features_from_text(text):
    
    # Dataframe creation
    lemmatized_text_list = []
    df = pd.DataFrame(columns=['Content'])
    df.loc[0] = text
    df['Content_Parsed_1'] = df['Content'].str.replace("\r", " ")
    df['Content_Parsed_1'] = df['Content_Parsed_1'].str.replace("\n", " ")
    df['Content_Parsed_1'] = df['Content_Parsed_1'].str.replace("    ", " ")
    df['Content_Parsed_1'] = df['Content_Parsed_1'].str.replace('"', '')
    df['Content_Parsed_2'] = df['Content_Parsed_1'].str.lower()
    df['Content_Parsed_3'] = df['Content_Parsed_2']
    for punct_sign in punctuation_signs:
        df['Content_Parsed_3'] = df['Content_Parsed_3'].str.replace(punct_sign, '')
    df['Content_Parsed_4'] = df['Content_Parsed_3'].str.replace("'s", "")
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_list = []
    text = df.loc[0]['Content_Parsed_4']
    text_words = text.split(" ")
    for word in text_words:
        lemmatized_list.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
    lemmatized_text = " ".join(lemmatized_list)    
    lemmatized_text_list.append(lemmatized_text)
    df['Content_Parsed_5'] = lemmatized_text_list
    df['Content_Parsed_6'] = df['Content_Parsed_5']
    for stop_word in stop_words:
        regex_stopword = r"\b" + stop_word + r"\b"
        df['Content_Parsed_6'] = df['Content_Parsed_6'].str.replace(regex_stopword, '')
    df = df['Content_Parsed_6']
    df = df.rename(columns={'Content_Parsed_6': 'Content_Parsed'})
    
    # TF-IDF
    features = tfidf.transform(df).toarray()
    
    return features
def get_category_name(category_id):
    for category, id_ in category_codes.items():    
        if id_ == category_id:
            return category

def predict_from_text(text):
    
    # Predict using the input model
    prediction_svc = svc_model.predict(create_features_from_text(text))[0]
    prediction_svc_proba = svc_model.predict_proba(create_features_from_text(text))[0]
    cp=prediction_svc_proba.max()*100
    print(cp)
    category_svc = get_category_name(prediction_svc)
    ct=category_svc
    if (cp < 90):
        ct='NA'
    # Return result
    else :
        ct = get_category_name(prediction_svc)
    f = open("category.txt", "w")
    f.write(ct)
    f.close()
    f1 = open("cat1.txt","w")
    f1.write(category_svc)
    f1.close()
    print("The predicted category using the SVM model is %s." %(category_svc) )
    print("The conditional probability is: %a" %(prediction_svc_proba.max()*100))

txt3='''Former Indian cricket team batsman Gautam Gambhir revealed his choices for an all-time India Test XI and he decided to go with Anil Kumble as the skipper of the side ahead of MS Dhoni and Virat Kohli. Both Dhoni and Kohli were part of the chosen side but Gambhir still went with Kumble whom he considers to be the best captain he has played under. Gambhir chose the legendary duo of Sunil Gavaskar and Virender Sehwag as his openers with Rahul Dravid coming out to bat on No. 3. The middle order comprised of Sachin Tendulkar, Virat Kohli, Kapil Dev in an all-rounder role and MS Dhoni as the wicket-keeper. Anil Kumble and Harbhajan Singh were the chosen spinners while the pace department included stalwarts Javagal Srinath and Zaheer Khan. READ: Mohammad Yousuf picks India stalwart as the best batsman currently “Sehwag and I were having dinner when Kumble walked in and said that you guys will open throughout the series no matter what. Even if you get 8 ducks it doesn’t matter. I have never heard such words from anyone in my career. So, if I have to give my life for someone, it would be Anil Kumble. Those words are still in my heart,” Gambhir told SportsTak during a recent interaction when asked to chose the best captain he has played under. “Had he captained India for a longer duration like Sourav Ganguly, MS Dhoni or Virat Kohli, he would have made many records. He captained in tough series’ in Australia and Sri Lanka,” Gambhir added. The interesting part of Gambhir’s team is the bowling line-up as the quartet played together for some time and all four were sort of mainstays for India in the late 1990s and the 2000s decade.
Top Image	'''
txt2='''As many as 1,074 Covid-19 patients have recovered in the last 24 hours, the highest number of recoveries recorded in one day, the health ministry said on Monday. Addressing a press briefing, Joint Secretary at the health ministry Lav Agarwal said the recovery rate stands at 27.52 per cent with 11,706 Covid-19 patients cured till now. In the last 24 hours, 1,074 Covid-19 patients have recovered, the highest number of recoveries in one day, Agarwal said. He further said the outcome ratio of Covid-19 -- the ratio of recoveries and deaths of closed cases -- was recorded at 90:20. “The outcome ratio on April 17 was 80:20 which is now 90:20 which can be seen as an improvement,” Agarwal said. In the last 24 hours, 2,553 Covid-19 cases were reported, taking the number of overall cases to 42,533, while the total active cases stand 29,453, he said. Agarwal also said that the Covid-19 curve is relatively flat as of now and it was not right to talk in terms of when the peak would come. “If we collectively work then peak might not ever come while if we fail in any way we might experience a spike in cases,” he said. Agarwal assured that there is no shortage of testing kits. “On Sunday, 57,474 tests were conducte. We have progressively increased our testing capacity as per need,” he said. Amitabh Kant, Chairman Empowered Group dealing with civil society, NGOs, industries and international partners, said in 112 aspirational districts, “we worked with the collectors and in these 112 districts only 610 cases have been reported which is 2 per cent of the national level infection”. In these 112 districts, 22 per cent of India’s population resides, he said. In a few districts like Baramulla, Nuh Rachi, YSR, Kupwara and Jaisalmer more than 30 cases have been reported, while in the rest of the places very few cases are there, Kant, who is also the CEO of NITI Aayog, said. Kant said the telemedicine service is now available on the Aarogya Setu application. He said 90 million people have installed the Aarogya Setu app till now. “Arogya Setu Mitra which has telemedicine features is also there,” he said. The mobile application helps users identify whether they are at risk of the Covid-19 infection. It also provides people with important information, including ways to avoid coronavirus infection and its symptoms. “The application enables people to assess the risk of exposure to Covid-19 infection based on their interaction with others, using cutting edge bluetooth technology, and artificial Intelligence enabled algorithms,” he said. Kant said the Empowered Group 6 has mobilised over 92,000 NGOs and CSOs and appealed them to assist state governments and district administrations in identifying hotspots and delivering essential services to the vulnerable including the homeless, daily wagers and migrant workers.'''
txt1='''ran says US push to extend Tehran’s arms embargo is ‘illegitimate’ Iran dismissed as “illegitimate” efforts by the United States to extend the U.N. Security Council arms embargo on Tehran, an Iranian Foreign Ministry spokesman said on Monday. “Iran is not seeking to exit the 2015 nuclear deal with six powers ... America’s move is illegitimate and our reaction will be proportionate,” Abbas Mousavi said in a televised weekly news conference. The United States said on Thursday it was “hopeful” the U.N. Security Council would extend the arms embargo on Iran before it expires in October. President Donald Trump’s administration has been taking a harder line with the United Nations over its desire to extend and strengthen the embargo on Iran. Washington has threatened to trigger a return of all U.N. sanctions on Iran as leverage to get backing from the 15-member Security Council on extending the U.N. arms embargo on Tehran. “The United States is not a member of the nuclear deal anymore ... Iran’s reaction to America’s illegal measures will be firm,” Mousavi said. Trump withdrew the United States from the Iran nuclear deal in 2018 and reimposed sanctions on Tehran that have crippled its economy. Under the deal, Iran agreed to halt its sensitive nuclear work in exchange for sanctions relief. Iran, which denies its nuclear program is aimed at building a bomb, has gradually rolled back its commitments under the accord since the United States quit. It argues that Washington’s actions justify such a course.'''
txt='''Shares took a turn for the worse on Monday as tensions between the Trump administration and China over the origins and handling of the coronavirus pandemic rattled investors. Benchmarks fell in most markets except for Australia, which was lifted by signs its own virus outbreak is being brought under control. India’s Sensex plunged nearly 6% as authorities extended their pandemic-fighting lockdown for another two weeks and new data showed an unprecedented drop in factory activity. Germany’s DAX dropped 3.3% to 10,507.33 and the CAC 40 in Paris lost 4% to 4,389.97. Britain’s FTSE 100 declined 0.5% to 5,735.00. The future for the S&P 500 slipped 1.1% and that for the Dow industrials lost 1.2%, pointing to a lower open on Wall Street. Tokyo, Shanghai and Bangkok were among markets closed for holidays. Stocks had closed broadly lower on Wall Street on Friday after Amazon and other big companies reported disappointing results. Criticized over his handling of the crisis, President Donald Trump has tried to shift the blame to China. Beijing has repeatedly pushed back on U.S. accusations that the outbreak was China’s fault. The antagonisms threaten to undo the truce in a trade war between Washington and Beijing that was struck just before China began shutting much of its economy down in late January to fight the pandemic. A 4-page Department of Homeland Security intelligence report dated May 1 and obtained by The Associated Press contends that Chinese leaders “intentionally concealed the severity” of the pandemic from the world in early January. It alleges, citing variances in trade patterns, that China was downplaying the severity of its outbreak, first reported in the central Chinese city of Wuhan, while stockpiling medical supplies. “The renewed possibility of the return of the trade war that had plagued markets since at least 2017 once again weighed on sentiment,” Jingyi Pan of IG said in a commentary. Tensions over the pandemic and threats to hit back with trade sanctions have amped up risk, Mizuho Bank said in a report. “Even as growth-stifling containment measures are set to be phased out in May, the global downturn looks to deepen in Q2,” it said, adding that anti-China threats from Trump, on top of record job losses, may result in a continuation of the “Mayday” type of fear dynamics. There is no public evidence of an intentional plot to buy up the world’s medical supplies, though China did muzzle doctors who warned of the virus early on. But it informed the World Health Organization of the outbreak on Dec. 31; contacted the U.S. Centers for Disease Control on Jan. 3 and publicly identified the pathogen as a novel coronavirus on Jan. 8. Many of its missteps appear to have stemmed from bureaucratic hurdles. Wall Street has been bracing for a poor showing by companies this earnings season due to the economic shock from the coronavirus. Many companies have pulled their earnings guidance for the rest of the year, citing uncertainty about how much of an impact the outbreak will have on their business and the economy, which is now in a recession. Bleak trade and manufacturing data are also discouraging investors on the lookout for upbeat news on steps to stop the pandemic and prevent a resurgence in cases in places that are beginning to reopen after shutdowns. Hong Kong’s Hang Seng index fell 4.2% to 23,613.80 on Monday. The Kospi in South Korea dropped 2.7% to 1,895.37. Shares also fell by more than 2% in Singapore, Taiwan and Jakarta. Australia’s S&P ASX/200 gained 1.4% to 5,320.30, rebounding from early losses on gains in miners and banks. The yield on the 10-year Treasury edged lower, to 0.60% from 0.62% on Friday, well below its 1.90% level at the start of the year. Benchmark U.S. crude oil fell $1.39 to $18.39 per barrel in electronic trading on the New York Mercantile Exchange. It gained 94 cents on Friday to $19.78 per barrel. U.S. crude has plunged from its perch of roughly $60 at the start of the year on worries about a collapse in demand and strained storage facilities. Brent crude, the international standard, gave up 56 cents to $25.88 per barrel. The dollar fetched 106.74 Japanese yen, down from 106.88 yen on Friday. The euro weakened to $1.0939 from $1.0980.'''
txt4='''Bihar Congress MLC Prem Chandra Mishra on Tuesday sent a legal notice to state Deputy Chief Minister Sushil Modi, who had claimed that Congress and RJD MLAs have not made any contribution to the Chief Minister’s Relief Fund (CMRF). In a tweet on Monday, Modi had said that the MLAs of RJD and Congress have not contributed a single rupee to the CMRF. “I had asked Sushil Modi to tender an apology to the Congress leaders over his remark and delete his untrue tweets. However, he has not withdrawn the tweets or tendered any apologies. Therefore, I have sent a legal notice to Sushil Modi,” said Mishra in a video message. Mishra said that Sushil Modi’s remark that Congress MLAs have not contributed anything to the Chief Minister Relief Fund are “blatant lies”. “Through the legal notice sent to Sushil Modi, I have asked him how he can lie about Chief Minister Relief Fund despite being the Deputy Chief Minister and Finance Minister of the state, that too at a time of such crisis,” he said. The legal notice said that the allegations made by Modi are “baseless” and with “mala fide intentions” to defame the Congress leaders and added that the donation has become a “political issue” for him. “Your actions amount to the commission of the offence of the defamation under Section 499 (defamation) as well as are actionable by the way of a civil proceeding,” the notice said. “That my client, being of a forgiving disposition, is willing to compound your offence if you immediately withdraw your defamatory and untrue tweet and issue a public apology through the same forum, failing which I have the instructions to initiate civil and criminal proceedings as per the law of the land,” it added. Mishra said that Bihar Youth Congress vice president Kumar Rohit has also filed a complaint to the Superintendent of Police over Sushil Modi’s remark and sought actions against him.'''
f=open('RL.txt','r')
txt=f.read()

predict_from_text(txt)