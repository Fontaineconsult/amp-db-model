import sys
sys.path.append("/home/daniel/dev/py36-venv/dev")

from amp_dprc_dbase.sf_cap_db import get_dbase_session, Student, Instructor, Course, Enrollment, CourseIlearnID
import sqlalchemy.orm.exc as db_error
import datetime, traceback
from sqlalchemy.dialects import postgresql

session = get_dbase_session()

def get_all_students_ids():
    query = session.query(Student).all()

    student_ids = []
    for each_student in query:
        student_ids.append(each_student.student_id)
    return student_ids


def check_or_commit_instructor(instructor_data):

    try:
        instructor_query = session.query(Instructor).filter_by(instructor_id=instructor_data["instructor_id"]).one()
        print("already found instructor")
    except db_error.NoResultFound:
        new_instructor = Instructor(instructor_id=instructor_data["instructor_id"],
                                        instructor_first_name=instructor_data["instructor_first_name"],
                                        instructor_last_name=instructor_data["instructor_last_name"],
                                        instructor_email=instructor_data["instructor_email"],
                                        instructor_phone=instructor_data["instructor_phone"])

        try:
            session.add(new_instructor)
            session.commit()
        except:
            session.rollback()
            print("Something went wrong with the instructor")


def check_or_commit_course(course_data):

    try:
        course_query = session.query(Course).filter_by(course_gen_id=course_data["course_gen_id"]).one()
        print("already found course")

    except db_error.NoResultFound:
        new_course = Course(course_gen_id=course_data["course_gen_id"],
                            course_name=course_data["course_name"],
                            course_section=course_data["course_section"],
                            course_instructor_id=course_data["course_instructor_id"],
                            semester=course_data["semester"],
                            course_online=course_data["course_online"],
                            import_date=datetime.datetime.utcnow()
                            )

        try:
            session.add(new_course)
            session.commit()
            print("saving course")
        except:
            session.rollback()
            print("Something went wrong with the course", traceback.print_exc())


def check_or_update_enrollement(student_id, course_gen_id, enrolled_status):

    try:
        # print(type(course_gen_id), type(student_id))
        #
        # course_check = session.query(Course).filter_by(course_gen_id=course_gen_id).one()
        #
        # student_check = session.query(Student).filter_by(student_id=student_id).one()
        #
        #course_id = course_check.id

        try:

            enrollement_check = session.query(Enrollment).filter_by(student_id=student_id,course_id=course_gen_id).one()
            enrollement_check.student_enrolled = enrolled_status
            session.commit()

        except db_error.NoResultFound:

            enrollement_commit = Enrollment(course_id=course_gen_id,
                                             student_id=student_id,
                                             student_enrolled=enrolled_status)
            session.add(enrollement_commit)
            session.commit()



    except db_error.NoResultFound:

        print(traceback.print_exc(),"course or student doesn't exist")
        pass


def commit_ilearn_id(course_id_pair):

    for each_pair in course_id_pair:
        print(each_pair)
        course_ilearn_id_commit = CourseIlearnID(ilearn_page_id=each_pair[0], course_gen_id=each_pair[1])
        session.add(course_ilearn_id_commit)
    session.commit()

def get_all_course_ilearn_ids(semester):
    ilearn_id_query = session.query(Course).filter_by(semester=semester).all()
    ilearn_ids = []
    for each in ilearn_id_query:
        print(each)
        if each.ilearn_page_id is not None:
            ilearn_ids.append((each.course_gen_id, each.ilearn_page_id.ilearn_page_id))
        else:
            continue
    return ilearn_ids





get_all_course_ilearn_ids("fa18")

