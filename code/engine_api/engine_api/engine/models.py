"""Engine models"""
import datetime as dt
import enum

from engine_api.database import Column, PkModel, db, relationship


class StatusEnum(enum.Enum):
    CREATED = 1
    LOADING_DATA = 2
    ANALYZING = 3
    READY = 4
    FAILURE = 5


def status_enum_to_string(enum_value):
    if enum_value == StatusEnum.CREATED:
        return 'CREATED'
    elif enum_value == StatusEnum.LOADING_DATA:
        return 'LOADING_DATA'
    elif enum_value == StatusEnum.ANALYZING:
        return 'ANALYZING'
    elif enum_value == StatusEnum.READY:
        return 'READY'
    else:
        return 'FAILURE'


class AnalysisRequest(PkModel):
    """A Sentiment Analysis request coming from Node.js"""

    __tablename__ = "analysis_request"
    keywords = Column(db.Text, nullable=False)  # TODO: using 'Text' type, once we implement a limit it can be switched to 'String()' type
    opened_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    status = Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.CREATED)
    # analysis complete
    twitter_analysis_complete = Column(db.Boolean, nullable=False, default=False)
    reddit_analysis_complete = Column(db.Boolean, nullable=False, default=False)
    tumblr_analysis_complete = Column(db.Boolean, nullable=False, default=False)
    # Text tables
    text_twitter = relationship("TextTwitter", back_populates="analysis_request")
    text_reddit = relationship("TextReddit", back_populates="analysis_request")
    text_tumblr = relationship("TextTumblr", back_populates="analysis_request")
    # AnalysisResults
    analysis_results = relationship("AnalysisResults", back_populates="analysis_request")

    def __init__(self, keywords, **kwargs):
        """Create instance."""
        super().__init__(keywords=keywords, **kwargs)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'keywords': self.keywords,
            'opened_at': self.opened_at.isoformat(),
            'status': status_enum_to_string(self.status),
            'twitter_analysis_complete': self.twitter_analysis_complete,
            'reddit_analysis_complete': self.reddit_analysis_complete,
            'tumblr_analysis_complete': self.tumblr_analysis_complete,
        }

    @property
    def get_status(self):
        """Current status of request as a string"""
        return status_enum_to_string(self.status)

    @property
    def analysis_complete(self):
        """True if Twitter, Reddit, and Tumblr analysis is complete, else false"""
        return self.twitter_analysis_complete and \
               self.reddit_analysis_complete and \
               self.tumblr_analysis_complete

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<AnalysisRequest({self.id!r})>"


class TextTwitter(PkModel):
    """Table that stores all Tweets related to an AnalysisRequest"""

    __tablename__ = "text_twitter"
    analysis_request_id = Column(db.Integer, db.ForeignKey("analysis_request.id"), nullable=False)
    analysis_request = relationship("AnalysisRequest", back_populates="text_twitter")
    created_at = Column(db.DateTime, nullable=False)
    text = Column(db.String(350), nullable=False)
    is_analyzed = Column(db.Boolean, nullable=False, default=False)

    def __init__(self, analysis_request_id, created_at, text, **kwargs):
        super().__init__(
            analysis_request_id=analysis_request_id,
            created_at=created_at,
            text=text,
            **kwargs
        )

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'analysis_request_id': self.analysis_request_id,
            'created_at': self.created_at.isoformat(),
            'text': self.text,
            'is_analyzed': self.is_analyzed
        }

    @property
    def get_date(self):
        """Return the Python Date object for the 'created_at' value"""
        return self.created_at.date()

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TextTwitter({self.id!r})>"


class TextReddit(PkModel):
    """Table that stores all Reddit posts/comments related to an AnalysisRequest"""

    __tablename__ = "text_reddit"
    analysis_request_id = Column(db.Integer, db.ForeignKey("analysis_request.id"), nullable=False)
    analysis_request = relationship("AnalysisRequest", back_populates="text_reddit")
    created_at = Column(db.DateTime, nullable=False)
    text = Column(db.Text, nullable=False)
    is_analyzed = Column(db.Boolean, nullable=False, default=False)

    def __init__(self, analysis_request_id, created_at, text, **kwargs):
        super().__init__(
            analysis_request_id=analysis_request_id,
            created_at=created_at,
            text=text,
            **kwargs
        )

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'analysis_request_id': self.analysis_request_id,
            'created_at': self.created_at.isoformat(),
            'text': self.text,
            'is_analyzed': self.is_analyzed
        }

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TextReddit({self.id!r})>"


class TextTumblr(PkModel):
    """Table that stores all Tumblr posts/comments related to an AnalysisRequest"""

    __tablename__ = "text_tumblr"
    analysis_request_id = Column(db.Integer, db.ForeignKey("analysis_request.id"), nullable=False)
    analysis_request = relationship("AnalysisRequest", back_populates="text_tumblr")
    created_at = Column(db.DateTime, nullable=False)
    text = Column(db.Text, nullable=False)
    is_analyzed = Column(db.Boolean, nullable=False, default=False)

    def __init__(self, analysis_request_id, created_at, text, **kwargs):
        super().__init__(
            analysis_request_id=analysis_request_id,
            created_at=created_at,
            text=text,
            **kwargs
        )

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'analysis_request_id': self.analysis_request_id,
            'created_at': self.created_at.isoformat(),
            'text': self.text,
            'is_analyzed': self.is_analyzed
        }

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TextTumblr({self.id!r})>"


class AnalysisResults(PkModel):
    """Table that stores the Analysis Results for an Analysis Request"""

    __tablename__ = "analysis_results"
    analysis_request_id = Column(db.Integer, db.ForeignKey("analysis_request.id"), nullable=False)
    analysis_request = relationship("AnalysisRequest", back_populates="analysis_results")
    result_day = Column(db.Date)
    # Twitter Result Values
    twitter_median = Column(db.Float(precision=32), nullable=True)
    twitter_average = Column(db.Float(precision=32), nullable=True)
    twitter_lower_quartile = Column(db.Float(precision=32), nullable=True)
    twitter_upper_quartile = Column(db.Float(precision=32), nullable=True)
    twitter_minimum = Column(db.Float(precision=32), nullable=True)
    twitter_maximum = Column(db.Float(precision=32), nullable=True)
    # Reddit Result Values
    reddit_median = Column(db.Float(precision=32), nullable=True)
    reddit_average = Column(db.Float(precision=32), nullable=True)
    reddit_lower_quartile = Column(db.Float(precision=32), nullable=True)
    reddit_upper_quartile = Column(db.Float(precision=32), nullable=True)
    reddit_minimum = Column(db.Float(precision=32), nullable=True)
    reddit_maximum = Column(db.Float(precision=32), nullable=True)
    # Tumblr Result Values
    tumblr_median = Column(db.Float(precision=32), nullable=True)
    tumblr_average = Column(db.Float(precision=32), nullable=True)
    tumblr_lower_quartile = Column(db.Float(precision=32), nullable=True)
    tumblr_upper_quartile = Column(db.Float(precision=32), nullable=True)
    tumblr_minimum = Column(db.Float(precision=32), nullable=True)
    tumblr_maximum = Column(db.Float(precision=32), nullable=True)

    def __init__(self, analysis_request_id, result_day, **kwargs):
        super().__init__(
            analysis_request_id=analysis_request_id,
            result_day=result_day,
            **kwargs
        )

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'analysis_request_id': self.analysis_request_id,
            'result_day': self.result_day.isoformat(),
            'twitter_median': self.twitter_median,
            'twitter_average': self.twitter_average,
            'twitter_lower_quartile': self.twitter_lower_quartile,
            'twitter_upper_quartile': self.twitter_upper_quartile,
            'twitter_minimum': self.twitter_minimum,
            'twitter_maximum': self.twitter_maximum,
            'reddit_median': self.reddit_median,
            'reddit_average': self.reddit_average,
            'reddit_lower_quartile': self.reddit_lower_quartile,
            'reddit_upper_quartile': self.reddit_upper_quartile,
            'reddit_minimum': self.reddit_minimum,
            'reddit_maximum': self.reddit_maximum,
            'tumblr_median': self.tumblr_median,
            'tumblr_average': self.tumblr_average,
            'tumblr_lower_quartile': self.tumblr_lower_quartile,
            'tumblr_upper_quartile': self.tumblr_upper_quartile,
            'tumblr_minimum': self.tumblr_minimum,
            'tumblr_maximum': self.tumblr_maximum
        }

    def __repr__(self):
        """Represent instance as a unique string"""
        return f"<AnalysisResults({self.id!r})>"
