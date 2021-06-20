from flask import Flask, render_template, redirect, url_for, current_app, request, sessions, flash
from werkzeug.utils import secure_filename
import random


import datetime
import os

# Db creds
# pwd - SubUser#$
# port - 5432

app = Flask(__name__)
app.config['SECRET_KEY'] = '09dd43f8d5fc56aec94e475e96205076'

admin = [{'user_id': 'jane', 'pass_wd': '1234'}, {'user_id': 'bane', 'pass_wd': '5678'}]
users = [{'user_id': 'tom', 'pass_wd': '123'}, {'user_id': 'tim', 'pass_wd': '456'}, {'user_id': 'ada', 'pass_wd': '789'}]

# This will show how Much Resource is available
max_capacity={
'instance': '50',
    'size': '20'
}
available_resorces={
    'instance': '50',
    'size': '20'
}

# This will show what all instance are currently running
running_resorces = []


# This will show request made for allocation
alloc_req=[]

# This will show allocation logs
allocation_details=[]


# add_env= {
#     'name': 'ali',
#     'email': 'ali123@gmail.com',
#     'instance': 10,
#     'size': 2,
#     'ec2_type': 't2'
# }

remove_env={
    'name': 'ali',
    'id': 'ali123@gmail.com',
    'instance': 10,
    'size': 2,
    'ec2_type': 't2'
}





@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        max_capacity['instance'] = str(int(max_capacity['instance']) + int(data['add_ins']))
        max_capacity['size'] = str(int(max_capacity['size']) + int(data['add_size']))
        available_resorces['instance'] = str(int(available_resorces['instance']) + int(data['add_ins']))
        available_resorces['size'] = str(int(available_resorces['size']) + int(data['add_size']))
        return  render_template('index1.html', avrs = available_resorces, mxcp = max_capacity)
    else:
        return render_template('index1.html', avrs=available_resorces, mxcp = max_capacity)



@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        add_env = request.form.to_dict()
        print('env si', add_env)
        for uzi in users:
            print('uzi si', uzi)
            if add_env['user_id'] == uzi['user_id'] and add_env['pass_wd'] == uzi['pass_wd'] and add_env['user_id'] == add_env['name']:
                print('env hi', add_env)
                uid = str(random.randint(1000, 9999))
                add_env['uid'] = uid
                print('data is', add_env)
                alloc_req.append(add_env)

                flash('Add request has been placed', 'success')
                return render_template('add.html', mxcp=max_capacity)
                #return redirect(url_for('add'), mxcp = max_capacity)
        else:
            flash('Incorrect Password', '')
            return render_template('add.html',mxcp = max_capacity)
    else:
        return  render_template('add.html',mxcp = max_capacity)


@app.route('/remove', methods=['POST', 'GET'])
def remove():
    #running_resorces = alloc_req
    if request.method == 'POST':
        print('bef', running_resorces)
        #running_resorces = alloc_req
        data = request.form.to_dict()
        print('andarhu',data)


        for uzi in admin:
            print('uzi si', uzi)
            if data['user_id'] == uzi['user_id'] and data['pass_wd'] == uzi['pass_wd']:
                for i in range(len(running_resorces)):
                    # print(i)
                    if running_resorces[i]['uid'] == data['uid']:
                        print('mai yaha')
                        available_resorces['instance'] = str(
                            int(available_resorces['instance']) + int(running_resorces[i]['instance']))
                        available_resorces['size'] = str(
                            int(available_resorces['size']) + int(running_resorces[i]['size']))
                        del running_resorces[i]
                        break
                print('aft', running_resorces)
                return render_template('remove.html',rrs = running_resorces)
        else:
            flash('Incorrect Password', '')
            print('aft', running_resorces)
            return render_template('remove.html', rrs=running_resorces)

    else:
        return render_template('remove.html', rrs=running_resorces)

                # add_env['uid'] = uid
                # print('data is', add_env)
                # alloc_req.append(add_env)
                #
                # flash('Add request has been placed', 'success')
                # return redirect(url_for('add'))
        # else:
        #     flash('Incorrect Password', '')
        #     return render_template('add.html')


        # for i in range(len(running_resorces)):
        #     # print(i)
        #     if running_resorces[i]['uid'] == data['uid']:
        #         print('mai yaha')
        #         available_resorces['instance'] = str(int(available_resorces['instance']) + int(running_resorces[i]['instance']))
        #         available_resorces['size'] = str(int(available_resorces['size']) + int(running_resorces[i]['size']))
        #         running_resorces.pop(i)
        #         break
        #
        # print('aft',running_resorces)
        # return render_template('remove.html',rrs = running_resorces)
    # else:
    #     return render_template('remove.html',rrs = running_resorces)


@app.route('/approve', methods=['GET','POST'])
def approve():
    if request.method == 'POST':
        print('bef', alloc_req)
        #running_resorces = alloc_req
        data = request.form.to_dict()
        print('andarhu',data)
        if data['action'] != 'deny':
            for uzi in admin:
                print('uzi si', uzi)
                if data['user_id'] == uzi['user_id'] and data['pass_wd'] == uzi['pass_wd']:
                    for i in range(len(alloc_req)):
                        # print(i)
                        if alloc_req[i]['uid'] == data['uid']:
                            print('mai yaha')
                            running_resorces.append(alloc_req[i])
                            available_resorces['instance'] = str(int(available_resorces['instance']) - int(alloc_req[i]['instance']))
                            available_resorces['size'] = str(int(available_resorces['size']) - int(alloc_req[i]['size']))
                            allocation_details.append(alloc_req[i])
                            alloc_req.pop(i)
                            break
                    print('aft',alloc_req)
                    return render_template('approve.html',allreq = alloc_req, avrs = available_resorces)
            else:
                flash('Incorrect Password', '')
                print('aft', alloc_req)
                return render_template('approve.html', allreq=alloc_req, avrs = available_resorces)
        else:
            for uzi in admin:
                print('uzi si', uzi)
                if data['user_id'] == uzi['user_id'] and data['pass_wd'] == uzi['pass_wd']:
                    for i in range(len(alloc_req)):
                        # print(i)
                        if alloc_req[i]['uid'] == data['uid']:
                            print('mai yaha')
                            #running_resorces.append(alloc_req[i])
                            #available_resorces['instance'] = str(int(available_resorces['instance']) - int(alloc_req[i]['instance']))
                            #available_resorces['size'] = str(int(available_resorces['size']) - int(alloc_req[i]['size']))
                            #allocation_details.append(alloc_req[i])
                            alloc_req.pop(i)
                            break
                    print('aft',alloc_req)
                    return render_template('approve.html',allreq = alloc_req, avrs = available_resorces)
            else:
                flash('Incorrect Password', '')
                print('aft', alloc_req)
                return render_template('approve.html', allreq=alloc_req, avrs = available_resorces)
    else:
        print(alloc_req)
        return  render_template('approve.html', allreq = alloc_req, avrs = available_resorces )





@app.route('/analyse', methods=['GET'])
def analyse():

    list2 = []
    count = []
    for i in range(len(allocation_details)):
        # x = list1[i]['name']

        if allocation_details[i]['name'] in list2:
            pass
        else:
            list2.append(allocation_details[i]['name'])
            # print('at',i,list1[i])

    for j in list2:
        x = 0
        for i in range(len(allocation_details)):
            if allocation_details[i]['name'] == j:
                x = x + 1
        count.append(x)
    return render_template('analyse.html', labels = list2, values = count)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user1 = request.form['fname']
        return redirect(url_for('user', usr=user1))
    else:
        return render_template('login.html')

@app.route('/prac', methods=['POST', 'GET'])
def prac():
    if request.method == 'POST':
        user1 = request.form.to_dict()
        print(user1)
        return render_template('practice.html')
    else:
        return render_template('practice.html')






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)