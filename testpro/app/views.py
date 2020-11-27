from django.shortcuts import render,HttpResponse,redirect
from .models import *
import datetime
from django.http.response import JsonResponse
from random import random
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.core import serializers
from django.core.mail import send_mail


# Create your views here.
def login(request):
	if request.method == 'POST':
		username=int(request.POST['usrname'])
		pswd=request.POST['paswd']
		try:
			user=Users.objects.get(username=username)
			if user.username==username and user.password==pswd:
				request.session['loginid']=user.username
				if user.role=="staff":
					return redirect('staffhome')
				elif user.role== 'hod':
					return redirect('hodhome')
				else:
					return redirect('home')
			else:
				return render(request,"login.html",{'passerror':'Incorrect Password'})
		except Users.DoesNotExist:
			return render(request,"login.html",{'usrerror':'Incorrect username'})
		
	else:
		return render(request,"login.html")

def admin(request):
	# admid=request.session['adminid']
	if 'adminid' not in request.session:
		return redirect('admin_login')
	else:
		return render(request,'admin.html')
		

def deptregn(request):
	if 'adminid' not in request.session:
		return redirect('admin_login')
	else:
		if request.method == 'POST':
			deptname=request.POST['dptname']
			deptid=int(request.POST['dptid'])
			data=Department(dept_name=deptname,dept_id=deptid)
			data.save()
			return render(request,'dept-regn.html',{'status': 'Registered Successfully'})

		else:
			return render(request,'dept-regn.html')

def deptmng(request):
	deptdata=Department.objects.all()
	return render(request,'manage-dept.html',{'deptdata':deptdata})

def usrregn(request):
	if request.method == 'POST':
		typusr=request.POST['usrtype']
		name=request.POST['usrname']
		usrid=int(request.POST['usrid'])
		doj=request.POST['joindate']
		dj=datetime.datetime.strptime(doj, '%m/%d/%Y').strftime('%Y-%m-%d')
		dob=request.POST['birthdate']
		db=datetime.datetime.strptime(dob, '%m/%d/%Y').strftime('%Y-%m-%d')
		deptname=request.POST['dpt_name']
		blood=request.POST['bldgrp']
		cntct=request.POST['phn']
		password=request.POST['password']
		image='download.png'
		checkuser=Users.objects.filter(username=usrid).exists()
		if checkuser==True:
			return render(request,'user-regn.html',{"error":"User Id already taken"})
		else:
			if typusr == "student":
				batch=request.POST['batchname']
				semdata=Batch.objects.get(name=batch,department=deptname)
				semester=semdata.semester
				userdata=Users(username=usrid,password=password,role=typusr)
				userdata.save()
				studdata=Student(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,batch=batch,designation=typusr,image=image,semester=semester)
				studdata.save()
				feedata=Fees(name=name,department=deptname,semester=semester,std_id=usrid,batch=batch,semtotal=25000)
				feedata.save()
		
			else:
				if 'sectioncharrge' in request.POST:
					sec=request.POST['sectioncharrge']
					userdata=Users(username=usrid,password=password,role=typusr)
					userdata.save()
					staffdata=Staff(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,sectionincharge=sec,designation=typusr,image=image)
					staffdata.save()
				else:
					userdata=Users(username=usrid,password=password,role=typusr)
					userdata.save()
					staffdata=Staff(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,designation=typusr,image=image)
					staffdata.save()
			deptdata=Department.objects.all()
			batchdata=Batch.objects.all()
			# send_mail(
    		# 	'subject',
			# 	'message body',
			# 	'your@djangoapp.com',
			# 	['kiransurya032@gmail.com'],
			# 	fail_silently=False,
			# )
			return render(request,'user-regn.html',{'status': 'Registered Successfully','deptdata':deptdata,'batchdata':batchdata})

	else:
		deptdata=Department.objects.all()
		batchdata=Batch.objects.all()
		return render(request,'user-regn.html',{'deptdata':deptdata,'batchdata':batchdata})

def admlogin(request):
	if request.method=='POST':
		username=request.POST['adminuser']
		password=request.POST['adminpassword']
		try:
			login=Admin.objects.get(username=username)
			if login.username == username and login.password == password:
				request.session['adminid']=login.id
				return redirect('admin_dashboard')
			else:
				return HttpResponse("Incorrect password")
		except Admin.DoesNotExist:
			return HttpResponse("Invalid username")
	else:
		return render(request,'admin-login.html')

def usrmng(request):
	stddata=Student.objects.all()
	stfdata=Staff.objects.all()
	return render(request,'manage-user.html',{'userdata':stddata,'staffdata':stfdata})

def dltbtch(request):
	return render(request,'dlt-batch.html')

# def viewusr(request):
# 	return render(request,'view-user.html')

def adminexam(request):
	deptdata=Department.objects.all()
	semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
	print(semdata)
	examdata=Exam.objects.values('examname','department','status','semester').annotate(cnt=Count('examname'))
	return render(request,'exam.html',{'examdata':examdata,'deptdata':deptdata,'semdata':semdata})

def adminfee(request):
	feedata=Fees.objects.all()
	print(feedata)
	return render(request,'fees-admin.html',{'feesdata':feedata})

def payfee(request,stdid,sem):
	feedata=Fees.objects.get(std_id=stdid)
	if sem==1:
		sumpaid=feedata.sem1paid
	elif sem==2:
		sumpaid=feedata.sem2paid
	elif sem==3:
		sumpaid=feedata.sem3paid
	elif sem==4:
		sumpaid=feedata.sem4paid
	elif sem==5:
		sumpaid=feedata.sem5paid
	elif sem==6:
		sumpaid=feedata.sem6paid


	# sumpaid=feedata.sem1paid+feedata.sem2paid+feedata.sem3paid+feedata.sem4paid+feedata.sem5paid+feedata.sem6paid
	print(sumpaid)
	return render(request,'fees-pay.html',{'feedata':feedata,'sem':sem,'totalpaid':sumpaid})
def paidfee(request):
	fee=request.POST['fees']
	sem=int(request.POST['semester'])
	if sem==1:
		studfeedata=Fees.objects.filter(std_id=stdid).update(sem1paid=fee)
		return redirect("adminviewfee")
	elif sem==2:
		studfeedata=Fees.objects.filter(std_id=stdid).update(sem2paid=fee)
		return HttpResponse("paid ")
	elif sem==3:
		studfeedata=Fees.objects.filter(std_id=stdid).update(sem3paid=fee)
		return HttpResponse("paid ")
	elif sem==4:
		studfeedata=Fees.objects.filter(std_id=stdid).update(sem4paid=fee)
		return HttpResponse("paid ")
	elif sem==5:
		studfeedata=Fees.objects.filter(std_id=stdid).update(sem5paid=fee)
		return HttpResponse("paid ")
	elif sem==6:
		studfeedata=Fees.objects.filter(std_id=stdid).update(sem6paid=fee)
		return HttpResponse("paid ")
	else:
		# Fees.objects.get(std_id=stdid).update()
		return HttpResponse("paid successfully")

def adminviewfee(request,stdid):
	# stdid=request.session['feeuserid']
	studfeedata=Fees.objects.get(std_id=stdid)
	totfee=25000
	balance=totfee-studfeedata.sem1paid
	print(balance)
	return render(request,'view-fees-admin.html',{'studfeedata':studfeedata})

def staffhome(request):
	return render(request,'staff-home.html')

def hodhome(request):
	return render(request,'hod-home.html')

def userprofile(request):
	id=request.session['loginid']
	user=Users.objects.get(username=id)
	# return HttpResponse(user.role)
	if user.role=='student':
		userdata=Student.objects.get(usr_id=id)
		return render(request,'profile.html',{'userdata':userdata})
	else:
		userdata=Staff.objects.get(usr_id=id)
		return render(request,'profile.html',{'userdata':userdata})

def staffexam(request):
	return render(request, 'exam-staff.html')
def hodexam(request):
	return render(request, 'hod-exam.html')

def feestaff(request):
	return render(request,'fee-staff.html')

def staffbook(request):
	userid=request.session['loginid']
	userdata=Staff.objects.get(usr_id=userid)
	dept=userdata.department
	bookdata=Book.objects.filter(department=dept)
	return render(request,"staff-book.html",{'bookdata':bookdata})
	# return HttpResponse("test")

def viewresult(request):
	if request.method=='POST':
		examname=request.POST['examname']
		department=request.POST['department']
		sem=request.POST['semester']
		result=Result.objects.filter(examname=examname,department=department,semester=sem)
		id=request.session['loginid']
		staffdata=Staff.objects.get(usr_id=id)
		# print(staffdata.designation)
		semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
		deptdata=Department.objects.all()
		
		if staffdata.designation == 'hod':
			inputdata=Exam.objects.values('examname').annotate(dcount=Count('semester')).filter(department=staffdata.department)
			return render(request,"hod-result-display.html",{'result':result,'inputdata':inputdata,'semdata':semdata,'deptdata':deptdata})
		else:
			inputdata=Exam.objects.values('examname').annotate(dcount=Count('semester')).filter(staffid=id)
			return render(request,"resultdisplay.html",{'result':result,'inputdata':inputdata,'semdata':semdata,'deptdata':deptdata})
	else:
		
		id=request.session['loginid']
		staffdata=Staff.objects.get(usr_id=id)
		# print(staffdata.designation)
		if staffdata.designation == 'hod':
			semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
			deptdata=Department.objects.all()
			inputdata=Exam.objects.values('examname').annotate(dcount=Count('semester')).filter(department= staffdata.department)
			return render(request,"viewresult_hod.html",{'inputdata':inputdata,'semdata':semdata,'deptdata':deptdata})
		else:
			
			deptdata=Department.objects.all()
			semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
			inputdata=Exam.objects.values('examname').annotate(dcount=Count('semester')).filter(staffid=id)
			return render(request,"viewresult_staff.html",{'inputdata':inputdata,'semdata':semdata,'deptdata':deptdata})

def manageexam(request):
	if request.method=='POST':
		examname=request.POST['examname']
		request.session['exam']=examname
		request.session['deptname']=request.POST['dpt_name']
		request.session['semester']=request.POST['semester']
		return redirect('createexam')	
	else:
		semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
		deptdata=Department.objects.all()
		examdata=Exam.objects.values('examname','department','semester','status').annotate(cnt=Count('examname'))
		return render(request,"mng-exam.html",{'deptdata':deptdata,'semesterdata':semdata,'examdata':examdata})
		
def hodmanageexam(request):
	if request.method=='POST':
		examname=request.POST['examname']
		request.session['exam']=examname
		request.session['deptname']=request.POST['dpt_name']
		request.session['semester']=request.POST['semester']
		return redirect('hodcreateexam')	
	else:
		semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
		deptdata=Department.objects.all()
		examdata=Exam.objects.values('examname','department','semester','status').annotate(cnt=Count('examname'))
		print(examdata)
		return render(request,"hod-manage-exam.html",{'deptdata':deptdata,'semesterdata':semdata,'examdata':examdata})

def examactive(request,examname):
	enableexam=Exam.objects.filter(examname=examname).update(status='enabled')
	id=request.session['loginid']
	stfdata=Users.objects.get(username=id)
	if stfdata.role=='hod':
		return redirect('hodmanageexam')
	else:
		return redirect('Manageexam')
def examdeactivate(request,examname):
	disableexam=Exam.objects.filter(examname=examname).update(status='disabled')
	id=request.session['loginid']
	stfdata=Users.objects.get(username=id)
	if stfdata.role=='hod':
		return redirect('hodmanageexam')
	else:
		return redirect('Manageexam')
def examdelete(request,examname):
	disableexam=Exam.objects.filter(examname=examname).delete()
	id=request.session['loginid']
	stfdata=Users.objects.get(username=id)
	if stfdata.role=='hod':
		return redirect('hodmanageexam')
	else:
		return redirect('Manageexam')
def createexam(request):
	if request.method=='POST':
		examname=request.session['exam']
		department=request.session['deptname']
		sem=request.session['semester']
		# return HttpResponse(sem)
		question=request.POST['question']
		# attachment=request.FILES['attachment']
		opt1=request.POST['opt1']
		opt2=request.POST['opt2']
		opt3=request.POST['opt3']
		opt4=request.POST['opt4']
		crctans=request.POST['crctans']
		if crctans=="opt1":
			crctopt=request.POST['opt1']
		elif crctans=="opt2":
			crctopt=request.POST['opt2']
		elif crctans=="opt3":
			crctopt=request.POST['opt3']
		else:
			crctopt=request.POST['opt4']
		examdata=Exam(examname=examname,department=department,question=question,opt1=opt1,opt2=opt2,opt3=opt3,opt4=opt4,crctopt=crctopt,subject='nil',semester=sem)
		examdata.save()
		try:
			examnxt=request.POST['nextexam']
			return redirect('createexam')
		except:
			return redirect('Manageexam')

	else:
		return render(request,"createexam.html")

def hodcreateexam(request):
	if request.method=='POST':
		examname=request.session['exam']
		department=request.session['deptname']
		sem=request.session['semester']
		# return HttpResponse(sem)
		question=request.POST['question']
		# attachment=request.FILES['attachment']
		opt1=request.POST['opt1']
		opt2=request.POST['opt2']
		opt3=request.POST['opt3']
		opt4=request.POST['opt4']
		crctans=request.POST['crctans']
		if crctans=="opt1":
			crctopt=request.POST['opt1']
		elif crctans=="opt2":
			crctopt=request.POST['opt2']
		elif crctans=="opt3":
			crctopt=request.POST['opt3']
		else:
			crctopt=request.POST['opt4']
		examdata=Exam(examname=examname,department=department,question=question,opt1=opt1,opt2=opt2,opt3=opt3,opt4=opt4,crctopt=crctopt,subject='nil',semester=sem)
		examdata.save()
		try:
			examnxt=request.POST['nextexam']
			return redirect('hodcreateexam')
		except:
			return redirect('hodmanageexam')

	else:
		return render(request,"hod-create-exam.html")

def stafffee(request):
	return render(request,"fee-staff.html")

def studexam(request):
	id=request.session['loginid']
	studdata=Student.objects.get(usr_id=id)
	dept=studdata.department
	sem=studdata.semester
	sem=studdata.semester
	examdata=Exam.objects.values('examname').annotate(dcount=Count('examname')).filter(department=dept,semester=sem,status='enabled')
	resultdata=Result.objects.filter(student_id=id)
	# for exmdata in examdata:
	# 	for rsltdata in resultdata:
	# 		if rsltdata.examname == exmdata.examname
	# 			pass
	# 		else:
	# 			availexam=
	# print(examdata)
	return render(request,"stud-exam.html",{'result':resultdata,'examdata':examdata})

def studfee(request):
	stdid=request.session['loginid']
	feedata=Fees.objects.get(std_id=stdid)
	print(feedata)
	return render(request,"stud-fee.html",{'userfee':feedata})

# def studlogin(request):
# 	return render(request,"stud-login.html")

def home(request):
	return render(request,"stud-home.html")

def batchreg(request):
	if request.method == 'POST':
		btchname=request.POST['btchname']
		dept=request.POST['dpt_name']
		data=Batch(name=btchname,department=dept)
		data.save()
		deptdata=Department.objects.all()
		return render(request,'batch-register.html',{'status': 'Registered Successfully','deptdata':deptdata})
	else:
		deptdata=Department.objects.all()
		return render(request,"batch-register.html",{'deptdata':deptdata})
def batchmanage(request):
	batchdata=Batch.objects.all()
	return render(request,"batch-manage.html",{'batchdata':batchdata})

def batchdel(request,id):
	Batch.objects.get(id=id).delete()
	return redirect('batchmanage')
	# if request.method == 'POST':
	# 	btchname=request.POST['data']

def batchupdate(request,id):
	if request.method=='POST':
		batchname=request.POST['btchname']
		department=request.POST['dpt_name']
		semester=request.POST['semester']
		Batch.objects.filter(id=id).update(name=batchname,department=department,semester=semester)
		Student.objects.filter(department=department,batch=batchname).update(semester=semester)
		return redirect('batchmanage')

	else:
		batchdata=Batch.objects.get(id=id)
		deptdata=Department.objects.all()
		return render(request,"batch-edit.html",{'batchdata':batchdata,'deptdata':deptdata})


def admlogout(request):
    del request.session['adminid']
    return redirect('admin_login')

def dltdept(request,id):
	Department.objects.get(id=id).delete()
	return redirect('departmentmanage')

def updtdept(request,id):
	if request.method=='POST':
		deptid=request.POST['dptid']
		deptname=request.POST['dptname']
		Department.objects.filter(id=id).update(dept_name=deptname,dept_id=deptid)
		return redirect('departmentmanage')

	else:
		deptdata=Department.objects.get(id=id)
		return render(request,"dept-update.html",{'deptdata':deptdata})

def userlogout(request):
	del request.session['loginid']
	return redirect('login')

def studdel(request,id):
	Student.objects.get(usr_id=id).delete()
	Users.objects.get(username=id).delete()
	return redirect('usermanage')

def stfdel(request,id):
	Staff.objects.get(usr_id=id).delete()
	Users.objects.get(username=id).delete()
	return redirect('usermanage')

def userupdate(request,id):
	if request.method=='POST':
		# return HttpResponse("updated")
		typusr=request.POST['usrtype']
		name=request.POST['usrname']
		usrid=int(request.POST['usrid'])
		doj=request.POST['joindate']
		dj=datetime.datetime.strptime(doj, '%m/%d/%Y').strftime('%Y-%m-%d')
		dob=request.POST['birthdate']
		db=datetime.datetime.strptime(dob, '%m/%d/%Y').strftime('%Y-%m-%d')
		deptname=request.POST['dpt_name']
		blood=request.POST['bldgrp']
		cntct=request.POST['phn']

		# image='download.png'
		if typusr == "student":
			# try:
				# checkuser=Student.objects.filter(usr_id=id).exists()
			# if checkuser==True:
			batch=request.POST['batchname']
			semdata=Batch.objects.get(name=batch,department=deptname)
			print(semdata)
			print(semdata.semester)
			sem=semdata.semester
				# Student.objects.get(usr_id=id).delete()
				# Users.objects.get(username=id).delete()
			
			Student.objects.filter(usr_id=id).update(name=name,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,batch=batch,semester=sem)
				# userdata=Users(username=usrid,password=password,role=typusr)
				# userdata.save()
				# studdata=Student(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,batch=batch,designation=typusr,image=image,semester=semester)
				# studdata.save()
				
			# except Student.DoesNotExist:
			# 	batch=request.POST['batchname']
			# 	Staff.objects.get(usr_id=id).delete()
			# 	# Users.objects.get(username=id).delete()
			# 	Users.objects.get(username=id).update(username=usrid,role=typusr)
			# 	# userdata.save()
			# 	studdata=Student(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,batch=batch,designation=typusr)
			# 	studdata.save()
		else:
			# try:
			if 'sectioncharrge' in request.POST:
				sec=request.POST['sectioncharrge']
				Users.objects.filter(username=id).update(role=typusr)
				Staff.objects.filter(usr_id=id).update(name=name,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,sectionincharge=sec,designation=typusr)
			else:
				# Staff.objects.get(usr_id=id).delete()
				# Users.objects.get(username=id).delete()
				Users.objects.filter(username=id).update(role=typusr)
				# userdata.save()
				Staff.objects.filter(usr_id=id).update(name=name,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,designation=typusr)
			# except Staff.DoesNotExist:
			# 	Student.objects.get(usr_id=id).delete()
			# 	Users.objects.get(username=id).delete()
			# 	if 'sectioncharrge' in request.POST:
			# 		sec=request.POST['sectioncharrge']
			# 		userdata=Users(username=usrid,password=password,role=typusr)
			# 		userdata.save()
			# 		staffdata=Staff(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,sectionincharge=sec,designation=typusr,image=image)
			# 		staffdata.save()
			# 	else:
			# 		userdata=Users(username=usrid,password=password,role=typusr)
			# 		userdata.save()
			# 		staffdata=Staff(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,designation=typusr,image=image)
			# 		staffdata.save()
		return redirect('usermanage')
	else:
		userdetails=Users.objects.get(username=id)
		# return HttpResponse(userdetails.role)	
		dept=Department.objects.all()
		batch=Batch.objects.all()
		if userdetails.role=='student':
			studentdetails=Student.objects.get(usr_id=id)
			return render(request,"user-update.html",{ 'userdata':studentdetails,'department':dept,'batch':batch })
		else:
			staffdetails=Staff.objects.get(usr_id=id)
			return render(request,"user-update.html",{ 'userdata':staffdetails,'department':dept,'batch':batch })

def changepass(request):
	if request.method=="POST":
		password=request.POST['password']
		id=request.session['loginid']
		Users.objects.filter(username=id).update(password=password)
		if Users.objects.get(username=id).role == 'student':
			return redirect('home')
		else:
			return redirect('staffhome')
	else:
		return render(request,"changepassword.html")

# def checkpass(request):
# 	password=request.POST['pass']
# 	cnfpass=request.POST['cnfpass']
# 	if password == cnfpass:
# 		return JsonResponse({'message': "Password and confirmpassword is matching"})
# 	else:
# 		return JsonResponse({'message': "Password is mismatching"})

# def changeimg(request):
# 	fileup=request.FILES['fileupld']
# 	filename=str(random())+fileup.name
# 	fs=FileSystemStorage()
# 	fs.save(filename)

def changeimg(request):
	fileup=request.FILES['fileupld']
	filename=str(random())+fileup.name
	fs=FileSystemStorage(location='app/media/profileimage/',base_url='app/media/')
    # fs.save(filename,fileup)
	id = request.session['loginid']

	if Users.objects.get(username=id).role == 'student':
		fs.save(filename,fileup)
		Student.objects.filter(usr_id=id).update(image=filename)
		return redirect('profile')
	else:
		fs.save(filename,fileup)
		Staff.objects.filter(usr_id=id).update(image=filename)
		return redirect('profile')

def startexam(request, examname): 
	studentid=request.session['loginid']
	studentdata=Student.objects.get(usr_id=studentid)
	dept=studentdata.department
	sem=studentdata.semester
	examdata=Exam.objects.filter(department=dept,semester=sem,examname=examname).order_by('?')[:3]
	# try:
	# 	data=Exam.objects.filter(examname='testing')
	# except data.DoesNotExist:
	# 	print ("data not")

	# examsess=serializers.serialize('json', list(examdata))
	# request.session['questions']=examsess
	# print(type(examdata))
	return render(request,"attendexam.html",{'examdata':examdata})

def finishexam(request):
	totalmark=0
	for count in range(1,3):
		cnt=str(count)
		print(cnt)
		qusid=request.POST[cnt]
		# print(qusid)
		ans=request.POST[qusid]
	# x=request.POST['1']
	# print(x)
	# y=request.POST['2']
	# print(y)
	# z=request.POST['3']
	# print(z)
	# totalmark=1
		examdata=Exam.objects.get(id=int(qusid))
		examname=examdata.examname
		stdid=request.session['loginid']
		if examdata.crctopt==ans:
			totalmark+=1
		else:
			pass
	result=Result(student_id=stdid,examname=examname,mark=totalmark,status='finish')
	result.save()
	return render(request,"stud-examafter-rslt.html",{'mark':totalmark})

def mngbook(request):
	# deptdata=Department.objects.all()
	# for dept in deptdata:
	# 	for semester in 
	# 		sembookcnt=Book.objects.filter(department=dept.dept_name)
	# 		dptbookcnt=
	if request.method=='POST':
		bookname=request.POST['bkname']
		semester=request.POST['semester']
		dept=request.POST['department']
		bkfile=request.FILES['book']
		bkfilename=str(random())+bkfile.name
		fs=FileSystemStorage(location='app/media/books/',base_url='app/media/')
		fs.save(bkfilename,bkfile)
		bkdata=Book(bookname=bookname,department=dept,semester=semester,bookfilename=bkfilename)
		bkdata.save()
		deptdata=Department.objects.all()
		semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
		bookdata=Book.objects.all()
		return render(request,"manage-book.html",{'status':"book uploaded successfully",'bookdata':bookdata,'deptdata':deptdata,'semdata':semdata})

	else:
		
		deptdata=Department.objects.all()
		# print(Student.objects.values('semester').annotate(cnt=Count('semester'))[0])
		# semdata=Student.objects.all().values('semester')
		semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
		# semdata=Student.objects.annotate()group_by('semester'))
		bookdata=Book.objects.all()
		return render(request,"manage-book.html",{'bookdata':bookdata,'deptdata':deptdata,'semdata':semdata})

def studbook(request):
	userid=request.session['loginid']
	userdata=Student.objects.get(usr_id=userid)
	sem=userdata.semester
	dept=userdata.department
	bookdata=Book.objects.filter(department=dept,semester=sem)
	# bookdata=Book.objects.get(id=6)
	# for bk in bookdata:
	# print(bookdata.bookfilename)
	return render(request,"stud-book.html",{'bookdata':bookdata})