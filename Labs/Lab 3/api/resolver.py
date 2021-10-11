tempClasses = []
tempStudents = []


def student(_, info, id):
    for s in tempStudents:
        if s['id'] == id:
            return s
    return None


def students(_, info):
    return {
        'success': True,
        'errors': [],
        'students': tempStudents}


def classes(_, info, id):
    for c in tempClasses:
        if c['id'] == id:
            return c
    return None


def all_classes(_, info):
    return {
        'success': True,
        'errors': ['All Classes found.'],
        'classes': tempClasses}


def create_student(_, info, name, email):
    if len(tempStudents) == 0:
        id = 1
    else:
        id = tempStudents[-1]['id'] + 1
    s = {
        'id': id,
        'name': name,
        'email': email
    }
    tempStudents.append(s)
    return {
        'success': True,
        'errors': [],
        'students': [s]}


def get_student_ids():
    ids = []
    for s in tempStudents:
        ids.append(s['id'])
    return ids


def create_class(_, info, name, student_ids):
    ids = get_student_ids()
    for id in student_ids:
        if id not in ids:
            return {
                'success': False,
                'errors': ['Student of given id not found.'],
                'classes': None}
    if len(tempClasses) == 0:
        id = 1
    else:
        id = tempClasses[-1]['id'] + 1
    c = {
        'id': id,
        'name': name,
        'students': [tempStudents[i - 1] for i in student_ids]
    }
    tempClasses.append(c)
    return {
        'success': True,
        'errors': ['Class created.'],
        'classes': [c]}


def add_student_to_class(_, info, id, student_id):
    ids = get_student_ids()
    if student_id not in ids:
        return {
            'success': False,
            'errors': ['Student not found.'],
            'class': None}
    temp = None
    for s in tempStudents:
        if s['id'] == student_id:
            temp = s
            break
    if temp is not None:
        for c in tempClasses:
            if c['id'] == id:
                c['students'].append(temp)
                return {
                    'success': True,
                    'errors': [],
                    'class': c}
        return {'success': False,
                'errors': ['Class not found.'],
                'class': None}
    else:
        return {
            'success': False,
            'errors': ['Student not found.'],
            'class': None
        }
