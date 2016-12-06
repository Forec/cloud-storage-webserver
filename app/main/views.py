from datetime import datetime
from flask import render_template, session, redirect, url_for, \
    abort, flash, request, current_app, make_response
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, \
    FileForm, CommentForm, SearchForm, FileDeleteConfirmForm
from sqlalchemy import or_, and_
from .. import db
from ..models import User, Role, Permission, File, Comment, Message
from ..decorators import admin_required, permission_required

@main.route('/', methods=['GET', 'POST'])
def index():
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_files
    else:
        if current_user.is_authenticated:
            query = File.query.filter("private=0 or ownerid=:id").\
                filter("isdir=0").params(id=current_user.uid)
        else:
            query = File.query.filter("private=0")
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(File.created.desc()).paginate(
        page, per_page=current_app.config['ZENITH_FILES_PER_PAGE'],
        error_out=False
    )
    files = pagination.items
    return render_template('index.html', files = files,
                           pagination = pagination,
                           show_followed=show_followed)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@main.route('/user/<int:id>')
def user(id):
    user = User.query.filter_by(uid=id).first()
    if user is None:
        abort(404)
    files = user.files.filter_by(private=False)

    page_file = request.args.get('page_file', 1, type=int)

    pagination_file = files.order_by(File.created.desc()).paginate(
        page=page_file, per_page=current_app.config['PROFILE_ZENITH_FILES_PER_PAGE'],
        error_out=False
    )
    files = pagination_file.items
    return render_template('main/user.html', user = user, files= files,
                           pagination_post=pagination_file)


@main.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('您的资料已更新')
        return redirect(url_for('.user', id=current_user.uid))
    form.nickname.data = current_user.nickname
    form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.nickname = form.nickname.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('用户 ' + user.nickname +' 资料已更新')
        return redirect(url_for('.user',id=user.uid))
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.nickname.data = user.nickname
    form.about_me.data = user.about_me
    return render_template('main/edit_profile.html', form=form)

@main.route('/file/<int:id>', methods=['GET', 'POST'])
def file(id):
    file = File.query.get_or_404(id)
    form =CommentForm()
    if form.validate_on_submit():
        comment = Comment(body = form.body.data,
                          file = file,
                          author = current_user._get_current_object())
        db.session.add(comment)
        flash('您的评论已发布')
        return redirect(url_for('.file', id=file.uid, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (file.comments.count() - 1)// \
            current_app.config['ZENITH_COMMENTS_PER_PAGE'] + 1
    pagination = file.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['ZENITH_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('main/file.html', files=[file], comments = comments,
                           pagination = pagination, file = file, form = form,
                           moderate=current_user.can(Permission.MODERATE_COMMENTS))

@main.route('/follow/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(id):
    user = User.query.filter_by(uid=id).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('您已关注该用户')
        return redirect(url_for('.user', id=user.uid))
    current_user.follow(user)
    flash('您已关注用户 %s' % user.nickname)
    return redirect(url_for('.user', id=user.uid))


@main.route('/unfollow/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(id):
    user = User.query.filter_by(uid=id).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('您并未关注该用户')
        return redirect(url_for('.user', uid=id))
    current_user.unfollow(user)
    flash('您已取消对用户 %s 的关注' % user.nickname)
    return redirect(url_for('.user', uid=id))


@main.route('/followers/<int:id>')
def followers(id):
    user = User.query.filter_by(uid=id).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['ZENITH_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('main/followers.html', user=user, title="的关注者",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<int:id>')
def followed_by(id):
    user = User.query.filter_by(uid=id).first()
    if user is None:
        flash('不合法的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['ZENITH_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('main/followers.html', user=user, title="关注的人",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@main.route('/delete-file/<int:id>', methods=['GET','POST'])
@login_required
def delete_file(id):
    file= File.query.get_or_404(id)
    if current_user != file.owner and not current_user.can(Permission.ADMINISTER):
        abort(403)
    flash('小心！删除操作不能撤回！')
    form = FileDeleteConfirmForm()
    if form.validate_on_submit():
        if form.filename.data == '' or form.filename.data is None:
            flash("文件名不合法！")
            return redirect(url_for('.file', id=file.uid))
        file.filename = form.filename.name
        file.description = form.body.data
        file.path = form.path.data
        db.session.add(file)
        flash('文件信息已被更新')
        return redirect(url_for('.file',id = file.uid))
    form.body.data=file.description
    form.filename.data = file.filename
    form.path.data = file.path
    return render_template('main/confirm_delete_file.html',file = file,form=form,
                           token=current_user.generate_delete_token(fileid=id, expiration=3600))

@main.route('/delete-file-confirm/<token>')
@login_required
def delete_file_confirm(token):
    if current_user.delete_file(token):
        flash('文件已被删除')
        return redirect(url_for('main.cloud', path='/', direction='front', type='all'))
    else:
        abort(403)

@main.route('/rules')
def rules():
    return render_template('main/rules.html')

@main.route('/moderate_comments', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('main.moderate_comments', key=form.key.data))
    page = request.args.get('page', 1, type=int)
    key = request.args.get('key', '', type=str)
    if key == '':
        comment = Comment.query
    else:
        comment = Comment.query.filter(Comment.body.like('%'+key+'%'))
    pagination = comment.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['ZENITH_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    form.key.data = key
    return render_template('main/moderate_comments.html', comments=comments,
                           pagination=pagination, page=page, form=form)


@main.route('/moderate_comments/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate_comments',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate_comments/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate_comments',
                            page=request.args.get('page', 1, type=int)))

@main.route('/moderate_comments/disable_own/<int:id>')
@login_required
def moderate_comments_disable_own(id):
    comment = Comment.query.get_or_404(id)
    if comment.author == current_user or comment.file.owner == current_user:
        comment.disabled = True
        db.session.add(comment)
        flash('评论已被设置为不可见')
        return redirect(url_for('.file', id = comment.file_id))


@main.route('/moderate_files', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_files():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('main.moderate_files', key=form.key.data))
    page = request.args.get('page', 1, type=int)
    key = request.args.get('key', '', type=str)
    if key == '':
        file = File.query
    else:
        file = File.query.filter(or_(File.filename.like('%'+key+'%'), File.description.like('%'+key+'%')))
    pagination = file.order_by(File.created.desc()).paginate(
        page, per_page=current_app.config['ZENITH_FILES_PER_PAGE'],
        error_out=False)
    files = pagination.items
    form.key.data = key
    return render_template('main/moderate_files.html',files=files,
                           pagination=pagination, page=page, form=form)

@main.route('/moderate_files/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_files_delete(id):
    file = File.query.get_or_404(id)
    db.session.delete(file)
    return redirect(url_for('.moderate_files',
                            page=request.args.get('page', 1, type=int),
                            key = request.args.get('key', '', type=str)))

@main.route('/messages/')
@login_required
def message():
    uncheck_messages = current_user.recvMessages.order_by(Message.viewed.asc()).\
        order_by(Message.created.desc())
    page = request.args.get('page', 1, type=int)
    pagination = uncheck_messages.paginate(
        page, per_page=current_app.config['ZENITH_MESSAGES_PER_PAGE'],
        error_out=False
    )
    cur_messages = pagination.items
    return render_template('main/message.html', messages = cur_messages,
                           pagination = pagination)

videoList = ['.avi', '.mp4', '.mpeg', '.flv', '.rmvb', '.rm', '.wmv']
photoList = ['.jpg', '.jpeg', '.png', '.svg', '.bmp', '.psd']
docList = ['.doc', '.ppt', '.pptx', '.docx', '.xls', '.xlsx', '.txt', '.md',
               '.rst', '.note']
compressList = ['.rar', '.zip', '.gz', '.gzip', '.tar', '.7z']
musicList = ['.mp3', '.wav', '.wma', '.ogg']

def generateFileTypes(files):
    file_types = []
    for file in files:
        filetype = 'file'
        suffix = '.'+file.filename.split('.')[-1]
        if suffix in videoList:
            filetype = 'video'
        elif suffix in musicList:
            filetype = 'music'
        elif suffix == '.txt':
            filetype = 'txt'
        elif suffix == '.md' or suffix == '.rst':
            filetype = 'md'
        elif suffix == '.ppt' or suffix == '.pptx':
            filetype = 'ppt'
        elif suffix == '.xls' or suffix == '.xlsx':
            filetype = 'excel'
        elif suffix in docList:
            filetype = 'doc'
        elif suffix in photoList:
            filetype = 'photo'
        elif suffix in compressList:
            filetype = 'compress'
        file_types.append((file, filetype))
    if file_types == []:
        file_types = None
    return file_types


def generatePathList(p):
    ans = []
    parts = p.split('/')[:-1]
    sum = ''
    for i in range(0, len(parts)):
        parts[i] = parts[i] + '/'
        sum += parts[i]
        ans.append((sum, parts[i]))
    return ans

@main.route('/cloud/')
@login_required
def cloud():
    def generateFilelike(list):
        string = ""
        for suffix in list:
            string += "or filename like '%" + suffix + "' "
        return string[3:]
    type = request.args.get('type', 'all', type=str)
    path = request.args.get('path', '/', type=str)
    order = request.args.get('order', 'time', type=str)
    direction = request.args.get('direction', 'front', type=str)
    if path == '':
        path = '/'

    # check whether the path is valid
    if path != '/':
        if len(path.split('/')) < 3:
            abort(403)
        ___filename = path.split('/')[-2]
        ___filenameLen = -(len(___filename)+1)
        ___path = path[:___filenameLen]
        isPath = File.query.filter("path=:p and isdir=1 and filename=:f").\
            params(p=___path, f=___filename).first()
        if isPath is None or isPath.owner != current_user:
            abort(403)

    if type == 'video':
        query = current_user.files.filter(generateFilelike(videoList))
    elif type == 'document':
        query = current_user.files.filter(generateFilelike(docList))
    elif type == 'photo':
        query = current_user.files.filter(generateFilelike(photoList))
    elif type == 'music':
        query = current_user.files.filter(generateFilelike(musicList))
    elif type == 'compress':
        query = current_user.files.filter(generateFilelike(compressList))
    else:
        query = current_user.files.filter("path=:p").params(p=path)
    page = request.args.get('page', 1, type=int)
    if order == 'name':
        if direction == 'reverse':
            query = query.order_by(File.filename.desc())
        else:
            query = query.order_by(File.filename.asc())
    else:
        if direction == 'reverse':
            query = query.order_by(File.created.asc())
        else:
            query = query.order_by(File.created.desc())
    pagination = query.paginate(
        page, per_page=current_app.config['ZENITH_FILES_PER_PAGE'],
        error_out=False
    )
    files = pagination.items
    file_types = generateFileTypes(files)
    return render_template('main/cloud.html', files = file_types, _type=type, _order=order, curpath=path,
                          _direction=direction ,pagination = pagination, pathlists=generatePathList(path))

@main.route('/download/<int:id>')
@login_required
def download(id):
    return "TODO"

@main.route('/upload/')
@login_required
def upload():
    return 'TODO'

@main.route('/copy/')
@login_required
def copy():
    path = request.args.get('path', '/', type=str)
    if path == '':
        path='/'
    id = request.args.get('id', 0, type=int)
    if id <= 0:
        abort(403)
    file = File.query.get(id)
    if file is None or file.owner != current_user:
        abort(403)

    order = request.args.get('order', 'time', type=str)
    direction = request.args.get('direction', 'front', type=str)
    # check whether the path is valid
    if path != '/':
        if len(path.split('/')) < 3:
            abort(403)
        ___filename = path.split('/')[-2]
        ___filenameLen = -(len(___filename)+1)
        ___path = path[:___filenameLen]
        isPath = File.query.filter("path=:p and isdir=1 and filename=:f").\
            params(p=___path, f=___filename).first()
        if isPath is None or isPath.owner != current_user:
            abort(403)

    # fuck this duplicate code, I don't want to name it
    query = current_user.files.filter("path=:p and uid<>:id and isdir=1").\
        params(p=path, id=file.uid)
    page = request.args.get('page', 1, type=int)
    if order == 'name':
        if direction == 'reverse':
            query = query.order_by(File.filename.desc())
        else:
            query = query.order_by(File.filename.asc())
    else:
        if direction == 'reverse':
            query = query.order_by(File.created.asc())
        else:
            query = query.order_by(File.created.desc())
    pagination = query.paginate(
        page, per_page=current_app.config['ZENITH_FILES_PER_PAGE'],
        error_out=False
    )
    files = pagination.items
    file_types = generateFileTypes(files)
    return render_template('main/copy.html', _file=file, _path=path, files=file_types,_order=order,curpath=path,
                           _direction=direction, pagination = pagination, pathlists=generatePathList(path))

@main.route('/copy_check')
@login_required
def copy_check():
    pass

@main.route('/fork/')
@login_required
def fork():
    pass

@main.route('/newfolder/')
@login_required
def newfolder():
    pass