# !/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
__author__ = 'Tao Jiang'

from mongo_connect import *
import re
import datetime
import time

def format_degree(degree):
	"""
	format linkedin degree information
	:param degree:
	:return:
	"""
	if u"初中" in degree:
		degree = u"初中"
	elif u"高中" in degree or re.search("High school", degree,  re.I):
		degree = u"高中"
	elif u"中专" in degree:
		degree = u"中专"
	elif u"大专" in degree or re.search("junior college", degree, re.I):
		degree = u"大专"
	elif u"本科" in degree or u"学士" in degree or re.search("Diplom[ae]?", degree, re.I):
		degree = u"本科"
	elif u"专科" in degree:
		degree = u"专科"
	elif u"硕士" in degree or re.search("Master", degree, re.I):
		degree = u"硕士"
	elif u"博士" in degree or re.search("Ph\.?D", degree, re.I) or re.search("Doctor of Philosophy", degree, re.I) or re.search("Doctor", degree, re.I):
		degree = u"博士"
	elif re.search("Associate", degree, re.I):
		degree = "Associate"
	elif re.search("bachelor", degree, re.I) or re.search("B\.?A", degree, re.I) or re.search("B.\w.?", degree):
		degree = "Bachelor"
	elif re.search("M\.?B\.?A", degree, re.I) or re.search("Master of Business Administration", degree, re.I):
		degree = "MBA"
	else:
		degree = u"本科"

	return degree

def format_work_time(work_year):
	if re.match(u"^(\d+) 年 (\d+) 个月$", work_year):
		year = re.match(u"^(\d+) 年 (\d+) 个月$", work_year).group(1)
		mon = re.match(u"^(\d+) 年 (\d+) 个月$", work_year).group(2)
		work_year = str(int(year)*12+int(mon))
	if re.match(u"^(\d+) 个月$", work_year):
		mon = re.match(u"^(\d+) 个月$", work_year).group(1)
		work_year = str(mon)
	if re.match(u"^(\d+) 年$", work_year):
		year = re.match(u"^(\d+) 年$", work_year).group(1)
		work_year = str(int(year)*12)
	if re.match(u"不到 (\d+) 年", work_year):
		year = re.match(u"不到 (\d+) 年", work_year).group(1)
		work_year = str(int(int(year)*12*0.5)) + "-" + str(int(year)*12)
	return work_year

def test_xiugai():

	src_conn = connect("resume_test", "contact_resume_1_v1", host="192.168.3.221", port=27017, user="admin",password="abc@123")
	dest_conn = connect("2014", "linkedin_resume", host="192.168.3.224")

	page = 0
	page_size = 1000
	temp = 0
	all_temp = 0
	start_time = datetime.datetime.now()
	while True:
		db_cursor = src_conn.find({"source": u"举贤网"}).skip(page_size*page).limit(page_size)

		page += 1
		temp = 0
		for d in db_cursor:
			resume = {"resume_id": "", "cv_id": "", "phone": "", "name": "", "email": "", "create_time": long(0),
			  "crawled_time": long(0), "update_time": "", "resume_keyword": "", "resume_img": "",
			  "self_introduction": "", "expect_city": "", "expect_industry": "", "expect_salary": "",
			  "expect_position": "", "expect_job_type": "",
			  "expect_occupation": "", "starting_date": "", "gender": "", "age": "", "degree": "",
			  "enterprise_type": "", "work_status": "", "source": "", "college_name": "",
			  "profession_name": "", "last_enterprise_name": "", "last_position_name": "",
			  "last_enterprise_industry": "",
			  "last_enterprise_time": "", "last_enterprise_salary": "", "last_year_salary": "", "hometown": "",
			  "living": "", "birthday": "", "marital_status": "", "politics": "", "work_year": "",
			  "height": "", "interests": "", "career_goal": "", "specialty": "",
			  "special_skills": "", "drive_name": "", "country": "", "osExperience": "", "status": "0",
			  "flag": "0", "dimension_flag": False, "version": [], "keyword_id": [],
			  "resumeUpdateTimeList": [], "educationList": [], "workExperienceList": [], "projectList": [],
			  "trainList": [], "certificateList": [], "languageList": [], "skillList": [], "awardList": [],
			  "socialList": [], "schoolPositionList": [], "productList": [], "scholarshipList": []}

			# del d["_id"]
			# for k, v in d.items():
			# 	print k, resume[k]

			# for k, v in resume.items():
			#
			# 	print k, d[k]

			resume = d
			if "_id" in resume:
				del resume["_id"]

			last_enter_indus = resume.get("last_enterprise_industry").strip()
			if last_enter_indus != "":
				resume["last_enterprise_industry"] = last_enter_indus.replace(" ", ",")
				if len(resume["last_enterprise_industry"]) > 40:
					resume["last_enterprise_industry"] = ""
				print resume["last_enterprise_industry"]

			#
			# if resume.get("degree") != "":
			# 	# print resume["degree"]
			# 	resume["degree"] = format_degree(resume["degree"])
			#
			# for i in range(len(resume["educationList"])):
			# 	start = resume["educationList"][i].get("start_date").strip()
			# 	# print start
			# 	if start != "":
			# 			if re.match("^\d{4}$", start):
			# 				resume["educationList"][i]["start_date"] = start + "-09"
			#
			# 			elif re.match(u"(\d{4}) 年 (\d{1,2}) 月", start):
			# 				start_temp = re.match(u"(\d{4}) 年 (\d{1,2}) 月", start)
			# 				if len(start_temp.group(2)) == 1:
			# 					start_mon = "0" + start_temp.group(2)
			# 				else:
			# 					start_mon = start_temp.group(2)
			# 				resume["educationList"][i]["start_date"] = start_temp.group(1) + "-" + start_mon
			# 	end = resume["educationList"][i].get("end_date").strip()
			# 	if end != "":
			# 		if re.match("^\d{4}$", end):
			# 			resume["educationList"][i]["end_date"] = end + "-06"
			# 		elif re.match(u"(\d{4}) 年 (\d{1,2}) 月", end):
			# 			end_temp = re.match(u"(\d{4}) 年 (\d{1,2}) 月", end)
			# 			if len(end_temp.group(2)) == 1:
			# 					end_mon = "0" + end_temp.group(2)
			# 			else:
			# 				end_mon = end_temp.group(2)
			# 			resume["educationList"][i]["end_date"] = end_temp.group(1) + "-" + end_mon
			#
			# 	degree = resume["educationList"][i]["degree"]
			# 	if degree != "":
			# 		resume["educationList"][i]["degree"] = format_degree(degree)
			#
			# 	if resume["profession_name"] == "":
			# 		resume["profession_name"] = resume["educationList"][i]["profession_name"]
			# 	if resume["degree"] == "":
			# 		resume["degree"] = resume["educationList"][i]["degree"]
			# 	if resume["college_name"] == "":
			# 		resume["college_name"] = resume["educationList"][i]["college_name"]
			#
			# if "living" in resume:
			# 	resume["living"] = resume["living"].replace(" ", "")
			#
			# resume["status"] = "0"
			# resume["flag"] = "0"
			#
			# for i in range(len(resume["workExperienceList"])):
			# 	start = resume["workExperienceList"][i].get("start_date").strip()
			# 	if start != "":
			# 		if re.match("^\d{4}$", start):
			# 			resume["workExperienceList"][i]["start_date"] = start + "-03"
			#
			# 		elif re.match(u"(\d{4}) 年 (\d{1,2}) 月", start):
			# 			start_temp = re.match(u"(\d{4}) 年 (\d{1,2}) 月", start)
			# 			if len(start_temp.group(2)) == 1:
			# 				start_mon = "0" + start_temp.group(2)
			# 			else:
			# 				start_mon = start_temp.group(2)
			# 			resume["workExperienceList"][i]["start_date"] = start_temp.group(1) + "-" + start_mon
			#
			# 	end = resume["workExperienceList"][i].get("end_date").strip()
			# 	if end != "":
			# 		if re.match("^\d{4}$", end):
			# 			resume["workExperienceList"][i]["end_date"] = end + "-06"
			# 		elif re.match(u"(\d{4}) 年 (\d{1,2}) 月", end):
			# 			end_temp = re.match(u"(\d{4}) 年 (\d{1,2}) 月", end)
			# 			if len(end_temp.group(2)) == 1:
			# 					end_mon = "0" + end_temp.group(2)
			# 			else:
			# 				end_mon = end_temp.group(2)
			# 			resume["workExperienceList"][i]["end_date"] = end_temp.group(1) + "-" + end_mon
			# 	work_time = resume["workExperienceList"][i].get("work_time")
			# 	if work_time != "":
			# 		resume["workExperienceList"][i]["work_time"] = format_work_time(work_time)
			#
			# 	for i in range(len(resume["projectList"])):
			# 		end = resume["projectList"][i].get("end_date")
			# 		if end != "":
			# 			if re.match("^\d{4}$", end):
			# 				resume["projectList"][i]["end_date"] = end + "-06"
			# 			elif re.match(u"(\d{4}) 年 (\d{1,2}) 月", end):
			# 				end_temp = re.match(u"(\d{4}) 年 (\d{1,2}) 月", end)
			# 				if len(end_temp.group(2)) == 1:
			# 					end_mon = "0" + end_temp.group(2)
			# 				else:
			# 					end_mon = end_temp.group(2)
			# 				resume["projectList"][i]["end_date"] = end_temp.group(1) + "-" + end_mon
			# 			resume["projectList"][i]["start_date"] = resume["projectList"][i].get("end_date")
			#
			# 	for i in range(len(resume["awardList"])):
			# 		time_info = resume["awardList"][i].get("time")
			# 		if time_info != "":
			# 			if re.match("^\d{4}$", time_info):
			# 				resume["awardList"][i]["time"] = time_info + "-06"
			# 			elif re.match(u"(\d{4}) 年 (\d{1,2}) 月", time_info):
			# 				time_info_temp = re.match(u"(\d{4}) 年 (\d{1,2}) 月", time_info)
			# 				if len(time_info_temp.group(2)) == 1:
			# 					time_info_mon = "0" + time_info_temp.group(2)
			# 				else:
			# 					time_info_mon = time_info_temp.group(2)
			# 				resume["awardList"][i]["time"] = time_info_temp.group(1) + "-" + time_info_mon
			#
			# 	for i in range(len(resume["certificateList"])):
			# 		get_time = resume["certificateList"][i].get("get_time")
			# 		if get_time != "":
			# 			if re.match("^\d{4}$", get_time):
			# 				resume["certificateList"][i]["get_time"] = get_time + "-05"
			#
			# 			elif re.match(u"(\d{4}) 年 (\d{1,2}) 月", get_time):
			# 				get_time_temp = re.match(u"(\d{4}) 年 (\d{1,2}) 月", get_time)
			# 				if len(get_time_temp.group(2)) == 1:
			# 					get_time_mon = "0" + get_time_temp.group(2)
			# 				else:
			# 					get_time_mon = get_time_temp.group(2)
			# 				resume["certificateList"][i]["get_time"] = get_time_temp.group(1) + "-" + get_time_mon
			#
			# 	resume["publicationList"] = []

			# # 插入数据库
			# dest_conn.update({"cv_id": resume["cv_id"], "source": resume["source"]}, resume, True, False)
			
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