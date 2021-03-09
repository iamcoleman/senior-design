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
    keywords = Column(db.Text, nullable=False) # TODO: using 'Text' type, once we implement a limit it can be switched to 'String()' type
    opened_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    status = Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.CREATED)
    text_twitter = relationship("TextTwitter", back_populates="analysis_request")
    text_reddit = relationship("TextReddit", back_populates="analysis_request")

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
            'status': status_enum_to_string(self.status)
        }

    @property
    def get_status(self):
        """Current status of request"""
        return self.status

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<AnalysisRequest({self.id!r})>"


class TextTwitter(PkModel):
    """Table that stores all Tweets related to an AnalysisRequest"""
    """
    posted_at: DateTime
    text: String
    """

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

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TextTwitter({self.id!r})>"


class TextReddit(PkModel):
    """Table that stores all Reddit posts/comments related to an AnalysisRequest"""
    """
    posted_at: DateTime
    text: String
    """

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
