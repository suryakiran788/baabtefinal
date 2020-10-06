from django.shortcuts import render,HttpResponse,redirect
from .models import *
import datetime
from django.http.response import JsonResponse
from random import random
from django.core.files.storage import FileSystemStorage
from django.db.models import Count

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
				semester=request.POST['sem']
				userdata=Users(username=usrid,password=password,role=typusr)
				userdata.save()
				studdata=Student(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,batch=batch,designation=typusr,image=image,semester=semester)
				studdata.save()
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
	return render(request,'exam.html')

def adminfee(request):
	return render(request,'fees-admin.html')

def staffhome(request):
	return render(request,'user-home.html')

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

def feestaff(request):
	return render(request,'fee-staff.html')
def staffbook(request):
	return render(request,"staff-book.html")

def viewresult(request):
	return render(request,"viewresult_staff.html")

def manageexam(request):
	if request.method=='POST':
		examname=request.POST['examname']
		request.session['exam']=examname
		request.session['deptname']=request.POST['dpt_name']
		return redirect('createexam')	
	else:
		deptdata=Department.objects.all()
		return render(request,"mng-exam.html",{'deptdata':deptdata})

def createexam(request):
	if request.method=='POST':
		examname=request.session['exam']
		department=request.session['deptname']
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
		examdata=Exam(examname=examname,department=department,question=question,opt1=opt1,opt2=opt2,opt3=opt3,opt4=opt4,crctopt=crctopt,subject='nil')
		examdata.save()
		try:
			examnxt=request.POST['nextexam']
			return redirect('createexam')
		except:
			return redirect('Manageexam')

	else:
		return render(request,"createexam.html")

def stafffee(request):
	return render(request,"fee-staff.html")

def studexam(request):
	return render(request,"stud-exam.html")

def studfee(request):
	return render(request,"stud-fee.html")

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
		Batch.objects.filter(id=id).update(name=batchname,department=department)
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
		password=request.POST['password']
		image='download.png'
		if typusr == "student":
			try:
				# checkuser=Student.objects.filter(usr_id=id).exists()
			# if checkuser==True:
				batch=request.POST['batchname']
				semester=int(request.POST['sem'])
				Student.objects.get(usr_id=id).delete()
				Users.objects.get(username=id).delete()
				userdata=Users(username=usrid,password=password,role=typusr)
				userdata.save()
				studdata=Student(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,batch=batch,designation=typusr,image=image,semester=semester)
				studdata.save()
				
			except Student.DoesNotExist:
				batch=request.POST['batchname']
				Staff.objects.get(usr_id=id).delete()
				Users.objects.get(username=id).delete()
				userdata=Users(username=usrid,password=password,role=typusr)
				userdata.save()
				studdata=Student(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,batch=batch,designation=typusr,image=image)
				studdata.save()
		else:
			try:
				if 'sectioncharrge' in request.POST:
					sec=request.POST['sectioncharrge']
					# Users.objects.filter(username=id).update(username=usrid,password=password,role=typusr)
					Staff.objects.get(usr_id=id).delete()
					Users.objects.get(username=id).delete()
					userdata=Users(username=usrid,password=password,role=typusr)
					userdata.save()
					staffdata=Staff(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,sectionincharge=sec,designation=typusr,image=image)
					staffdata.save()
				else:
					Staff.objects.get(usr_id=id).delete()
					Users.objects.get(username=id).delete()
					userdata=Users(username=usrid,password=password,role=typusr)
					userdata.save()
					staffdata=Staff(name=name,usr_id=usrid,department=deptname,dateofbirth=db,blood_group=blood,phone=cntct,dateofjoin=dj,designation=typusr,image=image)
					staffdata.save()
			except Staff.DoesNotExist:
				Student.objects.get(usr_id=id).delete()
				Users.objects.get(username=id).delete()
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

def startexam(request):
	examdata=Exam.objects.filter(department='Mechanical')
	return render(request,"attendexam.html",{'examdata':examdata})

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
		bkdata=Book(bookname=bookname,department=dept,semester=semester)
		bkdata.save()
		deptdata=Department.objects.all()
		semdata=Student.objects.all().distinct()
		bookdata=Book.objects.all()
		return render(request,"manage-book.html",{'status':"book uploaded successfully",'bookdata':bookdata,'deptdata':deptdata,'semdata':semdata})

	else:
		
		deptdata=Department.objects.all()
		# print(Student.objects.values('semester').annotate(cnt=Count('semester'))[0])
		# semdata=Student.objects.all().values('semester')
		semdata=Student.objects.values('semester').annotate(dcount=Count('semester'))
		# semdata=Student.objects.annotate()group_by('semester'))
		bookdata=Book.objects.all()
		for sem in semdata:
			print(sem)
		return render(request,"manage-book.html",{'bookdata':bookdata,'deptdata':deptdata,'semdata':semdata})

def studbook(request):
	userid=request.session['loginid']
	userdata=Student.objects.get(usr_id=userid)
	sem=userdata.semester
	dept=userdata.department
	bookdata=Book.objects.filter(department=dept,semester=sem)
	return render(request,"stud-book.html",{'bookdata':bookdata})