from sqlalchemy import create_engine, and_, or_, not_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Date, Boolean, ARRAY, String
from datetime import date
import sys

Base = declarative_base()

class JobApplication(Base):
	__tablename__ = 'job_apps'

	ID = Column('ID', Integer, primary_key=True)
	app = Column('applied', Date, nullable=False)
	comp = Column('company', String, nullable=False)
	pos = Column('position', String, nullable=False)
	p_id = Column('position_id', String)
	country = Column('country', String, nullable=False)
	loc = Column('location', String)
	skills = Column('skills', ARRAY(String), nullable=False)
	portal = Column('portal', String, nullable=False)
	resp = Column('response', Boolean)
	status = Column('status', Text)

def get_count(session):
	return session.query(JobApplication).count()

def connect(c_str):
	engine = create_engine(c_str)
	Base.metadata.bind = engine
	Base.metadata.create_all(engine)
	DBSession = sessionmaker(bind=engine)
	print('Conncted to the database ...')
	return DBSession()

def insert_job(session, values):
	new_job = JobApplication(**values)
	session.add(new_job)
	session.commit()
	print('Inserted new row ...')

def get_jobs(session, param):
	return session.query(JobApplication).filter(JobApplication.comp.ilike(param['company'].lower())).all()

def update_job(session, company, position, status='', position_id=None, application_id=None):
	if position_id is None and application_id is None:
		rs = session.query(JobApplication).filter(JobApplication.comp.ilike(company.lower()),
			JobApplication.pos.ilike(position.lower())).all()
		if len(rs) > 1:
			print('Multiple results, need position or application ID')
			return 'Multiple results, need position or application ID'
		if len(rs) == 0:
			print('Unable to find application ...')
			return 'No result'
		else:
			job = None
			for job in rs:
				job.resp = True
				job.status = status

			session.commit()
			print('application_id:{} updated succesfully ...'.format(job.ID))
			return job.ID
	
	elif position_id is None:
		rs = session.query(JobApplication).filter_by(ID=application_id).all()
		if len(rs) == 0:
			print('Unable to find application ...')
			return 'No result'
		else:
			job = rs[0]
			job.resp = True
			job.status = status
			session.commit()
			print('application_id:{} updated succesfully ...'.format(job.ID))
			return job.ID

	elif application_id is None:
		rs = session.query(JobApplication).filter(JobApplication.comp.ilike(company.lower()),
			JobApplication.pos.ilike(position.lower()), JobApplication.p_id.ilike(position_id.lower())).all()
		if len(rs) > 1:
			print('Multiple results, need application ID')
			return 'Multiple results, need application ID'
		else:
			job = None
			for job in rs:
				job.resp = True
				job.status = status

			session.commit()
			print('application_id:{} updated succesfully ...'.format(job.ID))
			return job.ID

if __name__ == '__main__':
	

	# Session = DBSession()

	# app_det = {
	# 'app': date.today(),
	# 'comp': 'Microsoft',
	# 'pos': 'Software Engineer',
	# 'country': 'US',
	# 'skills': ['.Net','ASP','C#','C++'],
	# 'portal': 'Company Website',
	# 'resp': False,
	# 'loc': 'Seattle, WA'
	# }

	# new_job = JobApplication(**app_det)

	# Session.add(new_job)
	# Session.commit()

	# rs = Session.query(JobApplication).filter(and_(JobApplication.skills.any('Python'), JobApplication.skills.any('C++'))).all()
	# # print(rs)

	# for job in rs:
	# 	print(job.app)
	# 	print(job.comp)
	# 	print(job.pos)
	# 	if not job.p_id is None:
	# 		print(job.p_id)
	# 	print(job.skills)
	host, db, port, uname, pswd = [line.strip() for line in open('config','r').readlines()]
	c_str = 'postgresql://{}:{}@{}:{}/{}'.format(uname, pswd, host, port, db)
	session = connect(c_str)
	res = update_job(session, 'google', 'Software Engineer', status='Reject')
	session.close()