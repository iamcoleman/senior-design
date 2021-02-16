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


class AnalysisRequest(PkModel):
    """A Sentiment Analysis request coming from Node.js"""

    __tablename__ = "analysis_request"
    keywords = Column(db.Text, nullable=False) # TODO: using 'Text' type, once we implement a limit it can be switched to 'String()' type
    opened_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    status = Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.CREATED)
    # TODO: both text columns are placeholders, will eventually link to a Twitter/Reddit table that holds the text
    text_twitter = relationship("TextTwitter", back_populates="analysis_request")
    text_reddit = relationship("TextReddit", back_populates="analysis_request")

    def __init__(self, keywords, **kwargs):
        """Create instance."""
        super().__init__(keywords=keywords, **kwargs)

    def set_twitter_id(self, twitter_id):
        """Set the text_twitter ID"""
        # TODO: just changes the value to true for now
        self.text_twitter = True

    def set_reddit_id(self, reddit_id):
        """Set the text_reddit ID"""
        # TODO: just changes the value to true for now
        self.text_reddit = True

    @property
    def get_status(self):
        """Current status of request"""
        return self.status

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<AnalysisRequest({self.id!r})>"


class TextTwitter(PkModel):
    """Table that stores all Tweets related to an AnalysisRequest"""

    __tablename__ = "text_twitter"
    analysis_request_id = Column(db.Integer, db.ForeignKey("analysis_request.id"), nullable=False)
    analysis_request = relationship("AnalysisRequest", back_populates="text_twitter")

    def __init__(self, analysis_request_id, **kwargs):
        super().__init__(analysis_request_id=analysis_request_id, **kwargs)


class TextReddit(PkModel):
    """Table that stores all Reddit posts/comments related to an AnalysisRequest"""

    __tablename__ = "text_reddit"
    analysis_request_id = Column(db.Integer, db.ForeignKey("analysis_request.id"))
    analysis_request = relationship("AnalysisRequest", back_populates="text_reddit")
