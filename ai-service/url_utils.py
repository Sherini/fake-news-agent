from newspaper import Article

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        if article.text.strip() == "":
            return None

        return article.text

    except Exception as e:
        print("URL Error:", e)
        return None