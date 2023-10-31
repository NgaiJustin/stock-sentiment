# Abstract
Our project is building a data search/visualization tool for novice investors (or advanced investors who are new to a particular sector) to become more informed about market conditions that may affect their portfolios. To do this, we will aggregate news datasets to extract stories that pertain to financial markets and group them by which companies they apply to. We’ll apply a basic sentiment analysis to classify the events based on whether they should have a positive or negative impact on market expectations, and then join this time series with other financial data (like ticker prices). We’ll then display it in a form that is intuitive for the user and efficient in terms of compute resources used when processing queries.

# Problem/Planned Requirements
We will work with the following data:
* Multiple datasets with historical stock price data
    * we will look into combining these intelligently and organizing them offline
    * it may be difficult to get sufficient volume of data from free sources since many financial exchanges have paywalls for their datasets, but this will also allow us to practice our data cleaning and inspection skills
* “All the News 2.0” - 2M records on news articles from major sources
    * as a stretch goal, we could try to find more news datasets and combine them
    * however, we think that the deduplication and organization would be highly non trivial with news datasets so this is a stretch goal
* Additional datasets for sentiment analysis (Reddit, Twitter, etc.)
    * for each source, we’ll stream the data similar to what would be obtained with an API call

In terms of the search interface, users can either get databases for a particular ticker and time interval, or they can generate a “live” dashboard view which streams the historical data.

# Literature Review

### [Miriam Lux. 1997. Visualization of financial information. In Proceedings of the 1997 workshop on New paradigms in information visualization and manipulation (NPIV '97). Association for Computing Machinery, New York, NY, USA, 58–61.](https://doi.org/10.1145/275519.275532)

This paper discusses new methods for the graphical representation of financial information in a multi-dimensional manner. The representations discussed in the paper strive to enable users to get an overview of the global economy insight. The paper mentions that as with the nature of aggregate data, there is no natural and obvious physical representation, thus intuitive and comprehensible visual metaphors need to be developed. While the paper is rather dated, many of the discussed principles of visualization and insights in displaying financial information remain relevant in contemporary contexts. 

For example, the iceberg metaphor discussed in the paper (and in lecture) is particularly relevant in describing economic benchmarks—such as the gross national product (GNP), tax revenues, the national debt, and the unemployment rate etc. These only represent a very macroscopic view of the overall market and represent only the visible tip of a much larger and complex economic system, much like the tip of an iceberg that's visible above the water's surface. In the context of visualization, it is important to not only present what is on the surface but provide a comprehensive understanding of the entire economic situation that uncovers the majority of an iceberg's mass that lies beneath the water.

The paper introduces two distinct visualization approaches: geographic-centric and development-centric. In our project's specific context, we foresee the development-centric approach as being more relevant. This choice stems from our anticipation that users will harness our tools for company comparisons. By providing insights into growth stages and trajectories, this approach will empower them to make more informed decisions and draw valuable conclusions.



### [Mohammad Karim Sohrabi, Hosseion Azgomi, Parallel set similarity join on big data based on Locality-Sensitive Hashing, Science of Computer Programming,Volume 145, 2017, Pages 1-12, ISSN 0167-6423](https://doi.org/10.1016/j.scico.2017.04.006)

In lecture, we delved into techniques aimed at simplifying the process of joining multiple datasets. These methods include tools like FMSketch, which aids in estimating the count of unique elements within sets, helping us pinpoint keys for dataset joins. Additionally, locality-sensitive hashing techniques like Minhash facilitate the identification of overlaps across keys and the efficient calculation of Jaccard similarity. Lastly, data structures such as Bloom Filters enable the efficient merging of rows sharing the same key while minimizing disk I/O, a common bottleneck in such operations. 

This paper builds on these techniques discussed in class and explores the implementation of a new MapReduce based parallel method for set similarity joining that leverages locality sensitive hashing to speed up the similarity checking process. The paper explores many similarity functions including Jaccard similarity coefficient and others such as Sorensen–Dice coefficient and Cosine coefficient. 

Furthermore, the paper offers invaluable insights by presenting both pseudo and benchmark data for the MapReduce-based set similarity join. We intended to draw insights from these findings as they provide a solid foundation upon which we can base our own set similarity join implementation, streamlining our data processing and analysis tasks.



### [Theodore E. Christensen, Karson E. Fronk, Joshua A. Lee, Karen K. Nelson, Data visualization in 10-K filings, Journal of Accounting and Economics, 2023, 101631, ISSN 0165-4101](https://doi.org/10.1016/j.jacceco.2023.101631)

In this paper, the authors discuss recent trends in visualizing data from 10-K filings. Companies are required to file certain information with the SEC on a quarterly basis, and the 10-K provides valuable information to investors on the status of the company. However, the information in the 10-K forms can be difficult to process or fully understand. Similar to using bulleted lists and tables, infographics and charts are important ways to convey information in a less dense manner.
The authors analyze both quantitative and qualitative charts. They find that over half of the quantitative graphics are just bar charts, but that the number of charts used varies from industry to industry. They conclude that firms elect to use infographics when the information they want to share is more complex (as measured by future stock market volatility). One of the limitations of their work is that they don’t evaluate the honesty of the graphics
In developing this project, we considered scraping data from these 10-K filings in HTML form and displaying it as part of our dashboard. But we felt that the amount of data we could easily obtain might not be sufficient, since each company only files a 10-K once per quarter, so it would be poorly suited for online/streaming implementation tasks. Nevertheless, we will use the observations from this paper in order to ensure that our graphics are easy to understand and display relevant information for investors.


### [Xiaodong Li, Haoran Xie, Li Chen, Jianping Wang, Xiaotie Deng, News impact on stock price return via sentiment analysis, Knowledge-Based Systems, Volume 69, 2014, Pages 14-23, ISSN 0950-7051](https://doi.org/10.1016/j.knosys.2014.04.022)
In this paper, the authors perform some experiments on developing a sentiment analysis-based model for predicting stock prices. While we won’t focus on engineering the ML models to improve their accuracy, we think that this paper is relevant because it describes the theoretical foundations of sentiment analysis (which they also perform on financial news articles).
One interesting point is that sentiment analysis is parametrized on a sentiment dictionary. In this paper, the authors explore using two different dictionaries. One of the directions we can consider for scaling our system is to use multiple sentiment dictionaries, as some of them may have “blind spots” for a particular industry. We could try to combine the labels generated by each sentiment dictionary using the techniques covered in class.


We will refer to these four sources and others in order to gain the necessary background knowledge for our implementation tasks. Our work will be novel in terms of making financial data more accessible to people who are still familiarizing themselves with the basics of financial markets. Many existing financial software applications, like the desktop app for TD Ameritrade or Bloomberg Terminal, process streams of data that are known to be clean and display processed data streams that are useful for day traders. The main differences are:
our system will focus on easy-to-understand information (in particular, a stream of news headlines rather than a plot of a quantity like open interest in put/call options)
our system will be capable of processing messy data

