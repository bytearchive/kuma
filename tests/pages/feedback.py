from pages.article import ArticlePage


class FeedbackPage(ArticlePage):

    URL_TEMPLATE = '/{locale}/docs/MDN/Feedback'
    ARTICLE_NAME = 'Send feedback on MDN'
    ARTICLE_TITLE_SUFIX = " - The MDN project | MDN"
