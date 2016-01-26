# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Tao Jiang'

from mongo_connect import *
from handling_salary_time import *
import re
import datetime
import time


def test_xiugai():

	src_conn = connect("resume_test", "contact_resume_1_v1", host="192.168.3.221", port=27017, user="admin",password="abc@123")
	dest_conn = connect("2014", "lbtoo_resume", host="192.168.3.224")

	page = 0
	page_size = 1000
	temp = 0
	all_temp = 0
	start_time = datetime.datetime.now()
	while True:
		db_cursor = src_conn.find({"source": "Lbtoo"}).skip(page_size*page).limit(page_size)

		page += 1
		temp = 0
		for d in db_cursor:
			# resume = {"resume_id": "", "cv_id": "", "phone": "", "name": "", "email": "", "create_time": long(0),
			# 		  "crawled_time": long(0), "update_time": "", "resume_keyword": "", "resume_img": "",
			# 		  "self_introduction": "", "expect_city": "", "expect_industry": "", "expect_salary": "",
			# 		  "expect_position": "", "expect_job_type": "",
			# 		  "expect_occupation": "", "starting_date": "", "gender": "", "age": "", "degree": "",
			# 		  "enterprise_type": "", "work_status": "", "source": "", "college_name": "",
			# 		  "profession_name": "", "last_enterprise_name": "", "last_position_name": "",
			# 		  "last_enterprise_industry": "",
			# 		  "last_enterprise_time": "", "last_enterprise_salary": "", "last_year_salary": "", "hometown": "",
			# 		  "living": "", "birthday": "", "marital_status": "", "politics": "", "work_year": "",
			# 		  "height": "", "interests": "", "career_goal": "", "specialty": "",
			# 		  "special_skills": "", "drive_name": "", "country": "", "osExperience": "", "status": "0",
			# 		  "flag": "0", "dimension_flag": False, "version": [], "keyword_id": [],
			# 		  "resumeUpdateTimeList": [], "educationList": [], "workExperienceList": [], "projectList": [],
			# 		  "trainList": [], "certificateList": [], "languageList": [], "skillList": [], "awardList": [],
			# 		  "socialList": [], "schoolPositionList": [], "productList": [], "scholarshipList": []}
			# del d["_id"]
			# for k, v in d.items():
			# 	print k, resume[k]

			resume = d
			if "_id" in resume:
				del resume["_id"]
			if resume.get("hometown") != "":
				resume["hometown"] = resume["hometown"].replace("-", "").replace(" ", "")

			if resume.get("living") != "":
				resume["living"] = resume["living"].replace("-", "").replace(" ", "")

			resume["status"] = "0"
			resume["flag"] = "0"
			if resume.get("last_enterprise_salary") == "0":
				resume["last_enterprise_salary"] = ""

			if "<span" in resume["profession_name"]:
				resume["profession_name"] = resume["profession_name"].replace("<span class='highlight'>", "").replace("</span>", "")

			if resume["expect_salary"] == "0":
				resume["expect_salary"] = u"面议"
			if resume.get("last_year_salary") == "0":
				resume["last_year_salary"] = ""

			if resume["expect_city"] != "":
				resume["expect_city"] = resume["expect_city"].replace(u"、", ";").replace(u"，", ";")

			if resume["work_year"] != "":
				if re.match("^\d+$", resume["work_year"]):
					work_year = resume["work_year"]
					resume["work_year"] = str(int(work_year) * 12)
			if resume["skillList"] == [{"skill_name": "", "skill_degree": "", "skill_time": ""}]:
				resume["skillList"] = []

			resume["last_enterprise_time"] = ""

			for i in range(len(resume["workExperienceList"])):
				if resume["workExperienceList"][i].get("salary") == "0":
					resume["workExperienceList"][i]["salary"] = ""

				start = resume["workExperienceList"][i].get("start_date")
				if re.match("\d{4}-\d{2}", start):
					resume["workExperienceList"][i]["start_date"] = start
				elif re.match("\d{4}-\d", start):
					resume["workExperienceList"][i]["start_date"] = start[0:5] + "0" + start[5:]

				end = resume["workExperienceList"][i].get("end_date")
				if re.match("\d{4}-\d{2}", end):
					resume["workExperienceList"][i]["end_date"] = end
				elif re.match("\d{4}-\d", end):
					resume["workExperienceList"][i]["end_date"] = end[0:5] + "0" + end[5:]

				work_time = resume["workExperienceList"][i].get("work_time")
				resume["workExperienceList"][i]["work_time"] = handle_work_year(work_time)

			for i in range(len(resume["educationList"])):
				start = resume["educationList"][i].get("start_date")

				if re.match("\d{4}-\d{2}", start):
					resume["educationList"][i]["start_date"] = start
				elif re.match("\d{4}-\d", start):
					resume["educationList"][i]["start_date"] = start[0:5] + "0" + start[5:]

				end = resume["educationList"][i].get("end_date")
				if re.match("\d{4}-\d{2}", end):
					resume["educationList"][i]["end_date"] = end
				elif re.match("\d{4}-\d", end):
					resume["educationList"][i]["end_date"] = end[0:5] + "0" + end[5:]

				if "<span" in resume["educationList"][i]["profession_name"]:
					resume["educationList"][i]["profession_name"] = resume["educationList"][i]["profession_name"].replace("<span class='highlight'>", "").replace("</span>", "")

			# 插入数据库
			dest_conn.update({"cv_id": resume["cv_id"], "source": resume["source"]}, resume, True, False)
			
			temp += 1
			all_temp += 1
		end_time = datetime.datetime.now()
		print u"完成导入 %s 条数据，一共耗时 %d 秒 ！" % (all_temp, (end_time - start_time).seconds)
		# 判断是否是已经读取完数据，因为是分页查询的，每页1000条数据，若不满1000条则是最后的数据
		if temp % page_size != 0 or temp == 0:
			print u"---------- 已经导入所有数据"
			break


if __name__ == '__main__':
    test_xiugai()