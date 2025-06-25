import os
from pathlib import Path
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, ForeignKey, String
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv('DB_PATH') # Definir no .env como DB_PATH=src/db/sample.db

class DataBase:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def set_table_metadata(self, engine):
        metadata = MetaData()
        # Legislator Table Metadata
        Table(
            'legislator', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
        )
        # Bill Table Metadata
        Table(
            'bill', metadata,
            Column('id', Integer, primary_key=True),
            Column('title', String),
            Column('sponsor_id', Integer, ForeignKey('legislator.id')),
        )
        # Votes Table Metadata
        Table(
            'votes', metadata,
            Column('id', Integer, primary_key=True),
            Column('bill_id', Integer, ForeignKey('bill.id')),
        )
        # Vote Results Table Metadata
        Table(
            'vote_results', metadata,
            Column('id', Integer, primary_key=True),
            Column('legislator_id', Integer, ForeignKey('legislator.id')),
            Column('vote_id', Integer, ForeignKey('votes.id')),
            Column('vote_type', Integer, comment='vote_type=1 is In Favor, vote_type=2 is Against'),
        )
        # Create All
        metadata.create_all(engine)
        
    def create_engine_and_run_conversion_pipelines(self):
        db_uri = f'sqlite:///{DB_PATH}'
        
        if Path(DB_PATH).exists():
            return create_engine(db_uri)
        else:
            engine = create_engine(db_uri)
            self.set_table_metadata(engine)
            self.pipeline.run(engine)
            return engine
