import datetime
import logging
from typing import Dict, List, Type, Union

import git
from peewee import (
    BooleanField,
    DateField,
    DateTimeField,
    DoesNotExist,
    DoubleField,
    ForeignKeyField,
    IntegerField,
    IntegrityError,
    InternalError,
    Model,
    PostgresqlDatabase,
    PrimaryKeyField,
    TextField,
    TimeField, fn,
)

from modules import Config as Cfg
from modules import Methods
from modules.Credentials import DB, DB_HOST, DB_PORT, DB_USER, DB_PASS, UTC_TIME_ZONE

"""
в этом файле модели для всех таблиц бд
я создал BaseModel и наследовал все классы от нее
"""


db_handler = PostgresqlDatabase(
    DB, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS
)


class BaseModel(Model):
    # базовая модель, от нее наследованы все остальные модели
    class Meta:
        database = db_handler


class Admins(BaseModel):
    """
    тут абсолютно аналогично учителям описаны админы, которые тоже верифицируются по key
    """

    id = PrimaryKeyField(null=False)
    tg_id = TextField(null=True)
    name = TextField(null=True)

    class Meta:
        table_name = "admins"
        order_by = ("id",)


def delete_admin(id):
    print("Удаление")
    try:
        to_del = Admins.select().where(Admins.id == id).get()
        to_del.delete_instance()
        return True
    except DoesNotExist:
        return None


def get_admin_in_list(phone):
    """
    получает список админов с номером телефона phone
    """
    return Admins.select().where((Admins.phone_number) == phone)


def is_admin(tg_id):
    try:
        if Admins.select().where(Admins.tg_id == tg_id).get():
            return True
    except DoesNotExist:
        print("Не нашел")
        return False


def get_admins():
    """
    получает список всех админов
    """
    return Admins.select().execute()


def get_admin_by_id(tg_id):
    """
    получает список админов с телеграмм айди tg_id
    """
    return Admins.select().where(Admins.tg_id == tg_id)



def get_admin_by_id_one(tg_id):
    """
    получает список админов с телеграмм айди tg_id
    """
    try:
        return Admins.select().where(Admins.tg_id == tg_id).get()
    except DoesNotExist:
        return None


def set_admin_data(admin_id, tg_id, name):
    """
    верифицирует админа, устанавливает его имя (name) и телеграмм айди (tg_id)
    ищет в бд по уникальному айди (id)
    """
    adm = Admins.select().where(Admins.id == admin_id).get()
    adm.name = name
    adm.tg_id = str(tg_id)
    adm.save()


def register_admin(name, tg_id):
    """
    регистрирует в бд нового адми по его (phone) номеру телефона
    """
    row = Admins(name=name, tg_id=tg_id)
    row.save()
    logging.info(f"registered admin phone: {name} {tg_id}")


def get_admin_key(phone):
    """
    получает объект админа по его номеру телефона (phone)
    """
    return Admins.select().where(Admins.phone_number == phone).get().key





class Users(BaseModel):
    """
    этот класс описывает пользователя (клиента)
    учителя и админы тоже содержатся в этой бд
    id = уникальный айди
    tg_id = телеграм айди пользователя
    name = имя пользователя
    phone_number = номер телефона пользователя
    courseN_bought = куплен ли конкретный курс
    aboniment_freeze = дата заморозки абонемента (сначала NUll)
    aboniment_from = дата начала абонемента
    course_available = строка, айди купленных курсов через пробел
    aboniment_till = срок истечения абонемента
    """

    id = PrimaryKeyField()
    tg_id = IntegerField()
    name = TextField()
    phone_number = TextField()
    ts = DateTimeField(default=datetime.datetime.now)
    stage = IntegerField(null=True)
    start_funnel = TextField(null=True)

    class Meta:
        table_name = "users"
        order_by = ("id",)


def get_all_users_by_phone(query):
    return Users.select().where(Users.phone_number.contains(query)).limit(40)


def get_all_users(query):
    return Users.select()


def create_stage(user_id, stage):
    user: Users = Users.select().where(Users.id == user_id).get()
    user.stage = stage
    user.save()


def get_user_by_tg_id(tg_id) -> Union[Users, None]:
    try:
        return Users.select().where(Users.tg_id == tg_id).get()
    except (DoesNotExist, InternalError):
        return None

def update_phone_number(tg_id, phone_number):
    user = Users.select().where(Users.tg_id == tg_id).get()
    user.phone_number = phone_number
    user.save()

def get_user_by_id(id) -> Union[Users, None]:
    try:
        return Users.select().where(Users.id == id).get()
    except DoesNotExist:
        return None


def get_user_by_phone_number(phone) -> Union[Users, None]:
    try:
        return Users.select().where(Users.phone_number == phone).get()
    except DoesNotExist:
        return None


def login_new_client(tg_id, phone, name, funnel=None):
    """
    создает нового клиента в базе данных
    """

    row = Users(tg_id=str(tg_id), phone_number=phone, name=name, start_funnel=funnel)
    row.save()
    logging.info(f"Register user tg_id: {tg_id}, phone: {phone}, name: {name}")


def get_all_products():
    return Products.select()


def get_not_deleted_products():
    return Products.select().where(Products.is_deleted == False)


def get_not_deleted_products_search(query):
    return Products.select().where(Products.is_deleted == False, Products.name.contains(query))


def get_all_users():
    return Users.select()


def get_all_bought_products():
    return Products.select().join(Shoplist).distinct()


def get_segment_products():
    return Products.select().where(Products.id.in_([29, 30, 31, 32])).distinct()


def get_users_passed_entrance_test():
    return Users.select().join(UserAnswer).where(UserAnswer.questionnaire_question_answer.in_([1, 2, 3]))


def get_users_not_moms():
    return Users.select().join(UserAnswer).where(UserAnswer.questionnaire_question_answer.in_([3]))


def get_users_pregnant():
    return Users.select().join(UserAnswer).where(UserAnswer.questionnaire_question_answer.in_([2]))


def get_users_moms():
    return Users.select().join(UserAnswer).where(UserAnswer.questionnaire_question_answer.in_([1]))


def get_users_not_bought_product(product_id):
    return Users.select().join(Shoplist).where(Shoplist.product != product_id)


def get_users_bought_product(product_id):
    return Users.select().join(Shoplist).where(Shoplist.product == product_id)


def get_users_first_stage():
    return Users.select().where(Users.stage == 1)


def get_users_second_stage():
    return Users.select().where(Users.stage == 2)


def get_users_third_stage():
    return Users.select().where(Users.stage == 3)


class Categories(BaseModel):
    id = PrimaryKeyField(null=False)
    category = TextField(null=True)

    class Meta:
        table_name = "categories"
        order_by = ("id",)


def get_all_categories():
    return Categories.select()


def get_category_by_id(category_id):
    return Categories.select().where(Categories.id == category_id).get()


def edit_name_category(category_id, new_name):
    category = Categories.select().where(Categories.id == category_id).get()
    category.category = new_name
    category.save()
    return category


def create_category(category):
    c = Categories(category=category)
    c.save()


def rm_category_by_id(category_id):
    Categories.select().where(Categories.id == category_id).get().delete_instance()


class Lesson(BaseModel):
    id = PrimaryKeyField()
    content = TextField(null=True)
    photo = TextField(null=True)
    gif = TextField(null=True)
    document = TextField(null=True)
    start_date = TimeField(null=True)

    class Meta:
        table_name = "lesson"
        order_by = ("id",)


def get_lesson_by_id(lesson_id) -> Lesson:
    return Lesson.select().where(Lesson.id == lesson_id).get()


def save_lesson(content, photo, gif, document) -> Lesson:
    lesson = Lesson(content=content, photo=photo, gif=gif, document=document)
    lesson.save()
    return lesson


def edit_lesson(lesson_id, column_name, new_value):
    lesson: Lesson = Lesson.select().where(Lesson.id == lesson_id).get()
    if column_name == "content":
        lesson.content = new_value
    elif column_name == "photo":
        lesson.photo = new_value
    elif column_name == "gif":
        lesson.gif = new_value
    elif column_name == "document":
        lesson.document = new_value
    lesson.save()


class Products(BaseModel):
    """
    name = название товара
    description = описание товара
    price = цена товара
    """

    id = PrimaryKeyField(null=False)
    category = ForeignKeyField(Categories, field="id", on_delete="CASCADE")
    name = TextField()
    description = TextField(null=True)
    price = DoubleField(null=True)
    price_discount = DoubleField(null=True)
    image = TextField(null=True)
    link = TextField(null=True)
    content = TextField(null=True)
    is_deleted = BooleanField(default=False)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)

    class Meta:
        table_name = "products"
        order_by = ("id",)


def get_name_product(product_id):
    return Products.select().where(Products.id == product_id).get().name


def get_product_by_id(product_id) -> Union[Products, None]:
    try:
        product = Products.select().where(Products.id == product_id).get()
    except DoesNotExist:
        logging.info(f"A non-existing product was requested {product_id}")
        return None
    if product.is_deleted:
        logging.info(f"A product marked as deleted was requested {product_id}")
        return None
    else:
        return product


def get_products_by_category(category):
    return Products.select().where((Products.category == category) & (Products.is_deleted == False))


def get_products_by_curator(curator_id):
    return Products.select().join(ProductCurator).where(ProductCurator.curator == curator_id)


def save_product(category, name, description, price, image, link, content, price_discount) -> Products:
    product = Products(
        category=category,
        name=name,
        description=description,
        price=price,
        image=image,
        link=link,
        content=content,
        price_discount=price_discount,
    )
    product.save()
    return product


def edit_product(product_id, column_name, new_value):
    product: Products = Products.select().where(Products.id == product_id).get()
    if column_name == "name":
        product.name = new_value
    elif column_name == "description":
        product.description = new_value
    elif column_name == "price":
        product.price = new_value
    elif column_name == "price_discount":
        product.price_discount = new_value
    elif column_name == "image":
        product.image = new_value
    elif column_name == "link":
        product.link = new_value
    elif column_name == "content":
        product.content = new_value
    product.save()


def rm_product(product_id) -> bool:
    logging.info(f"Marking product as deleted {product_id}")
    product = get_product_by_id(product_id)
    product.is_deleted = True
    product.save()
    return True


class ProductLesson(BaseModel):
    id = PrimaryKeyField()
    product = ForeignKeyField(Products, field="id")
    lesson = ForeignKeyField(Lesson, field="id")
    order = IntegerField()

    class Meta:
        table_name = "product_lesson"
        order_by = ("id",)


def save_product_lesson(product_id, lesson_id, order=None) -> ProductLesson:
    product_lesson = ProductLesson(product=product_id, lesson=lesson_id, order=order)
    product_lesson.save()
    return product_lesson


def get_product_lesson_by_id(product_lesson_id) -> Union[ProductLesson, None]:
    try:
        return ProductLesson[product_lesson_id]
    except DoesNotExist:
        return None


def get_all_product_lessons_for_product(product_id) -> Union[List[ProductLesson], None]:
    return ProductLesson.select().where(ProductLesson.product == product_id).order_by(ProductLesson.order)


def get_product_lesson_by_product_and_lesson(product_id, lesson_id) -> Union[ProductLesson, None]:
    try:
        return (
            ProductLesson.select()
                .where((ProductLesson.product == product_id) & (ProductLesson.lesson == lesson_id))
                .get()
        )
    except DoesNotExist:
        return None


def get_product_lesson_by_product_and_order(product_id, order) -> Union[ProductLesson, None]:
    try:
        return (
            ProductLesson.select().where((ProductLesson.product == product_id) & (ProductLesson.order == order)).get()
        )
    except DoesNotExist:
        return None


def get_next_lesson_for_product_and_current_lesson(product_id, lesson_id_current) -> Union[Lesson, None]:
    product_lesson_current = get_product_lesson_by_product_and_lesson(product_id, lesson_id_current)
    product_lesson_next = get_product_lesson_by_product_and_order(product_id, product_lesson_current.order + 1)
    if product_lesson_next:
        lesson_next = get_lesson_by_id(product_lesson_next.lesson)
        return lesson_next
    else:
        return None


class Curator(BaseModel):
    """
    Curators table
    """

    id = PrimaryKeyField(null=False)
    tg_id = TextField(null=True)
    username = TextField(null=True)
    name = TextField(null=True)
    phone_number = TextField(null=True)

    class Meta:
        table_name = "curator"
        order_by = ("id",)


def save_curator(username) -> Curator:
    curator = Curator(username=username)
    curator.save()
    return curator


def get_all_curators():
    return Curator.select()


def get_curator_by_id(curator_id) -> Curator:
    return Curator.select().where(Curator.id == curator_id).get()


def edit_curator(curator_id, new_name=None, new_phone=None):
    curator: Curator = Curator.select().where(Curator.id == curator_id).get()
    if curator:
        if new_name:
            curator.username = new_name
        if new_phone:
            curator.phone_number = new_phone
    curator.save()


class ProductCurator(BaseModel):
    """
    Maps curators to products
    """

    id = PrimaryKeyField()
    product = ForeignKeyField(Products, field="id")
    curator = ForeignKeyField(Curator, field="id")

    class Meta:
        table_name = "product_curator"
        order_by = ("id",)


def save_product_curator(product_id, curator_id):
    pc = ProductCurator(product_id=product_id, curator_id=curator_id)
    pc.save()


def rm_product_curator(product_id, curator_id):
    ProductCurator.select().where(
        (ProductCurator.product == product_id) & (ProductCurator.curator == curator_id)
    ).get().delete_instance()


class Shoplist(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, field="id")
    product = ForeignKeyField(Products, field="id")
    curator = ForeignKeyField(Curator, field="id", null=True)
    ts = DateTimeField()
    price = DoubleField()

    class Meta:
        table_name = "shoplist"
        order_by = ("id",)


def delete_product_user(shop_id):
    us_pr = Shoplist.select().where(Shoplist.id == shop_id).get()
    us_pr.delete_instance()
    return True


def check_bought_products(user_id):
    try:
        return Shoplist.select().where(Shoplist.user == user_id)
    except DoesNotExist:
        return None


def check_bought_product_by_product_id(user_id, product_id):
    try:
        return Shoplist.select().where(Shoplist.user == user_id, Shoplist.product == product_id)
    except DoesNotExist:
        return None


def get_curators_by_user(user_id):
    try:
        return Curator.select().join(Shoplist).where(Shoplist.user == user_id)
    except DoesNotExist:
        return None


def get_curators_by_shoplist(user_id, product_id):
    try:
        return (
            Curator.select().join(Shoplist).where((Shoplist.user == user_id) & (Shoplist.product == product_id)).get()
        )
    except DoesNotExist:
        return None


def get_curator_by_product(product_id):
    try:
        return Curator.select().join(ProductCurator).where(ProductCurator.product == product_id).get()
    except DoesNotExist:
        return None


def is_buy_korset(user_id):
    try:
        return Shoplist.select().where(Shoplist.product == 30, Shoplist.user == user_id)
    except DoesNotExist:
        return None


# view of a curator's load by product
class CuratorLoad(BaseModel):
    product = ForeignKeyField(Products, field="id")
    curator = ForeignKeyField(Curator, field="id")
    load = IntegerField()

    class Meta:
        table_name = "curator_load"
        order_by = ("product_id", "load")


def get_least_loaded_curator_for_product(product_id, except_curator_id=None) -> Union[Curator, None]:
    try:
        return (
            Curator.select()
                .join(CuratorLoad)
                .where((CuratorLoad.product == product_id) & (Curator.id != except_curator_id))
                .order_by(CuratorLoad.load)
                .limit(1)
                .get()
        )
    except DoesNotExist:
        return None


def get_shoplist_without_curator() -> Shoplist:
    return Shoplist.select().where(Shoplist.curator.is_null(True))


def fill_curators_shoplist(product_id):
    shoplist = Shoplist.select().where(Shoplist.curator.is_null(True))
    for curator in shoplist:
        curator.curator = get_least_loaded_curator_for_product(product_id)
        curator.save()


def is_product_lead_by_curator(product_id, curator_id):
    """
    Checks if a product is lead by a curator
    """
    if ProductCurator.select().where((ProductCurator.product == product_id) & (ProductCurator.curator == curator_id)):
        return True
    return False


def update_curator_shoplist(user_id, product_id, curator_id):
    sh = Shoplist.select().where((Shoplist.user == user_id) & (Shoplist.product == product_id)).get()
    sh.curator = curator_id
    sh.save()


def rm_curator_by_id(curator_id):
    # reassign least loaded curators for users who have been assigned to the curator that is being deleted
    products = set()
    for product_curator in ProductCurator.select().where(ProductCurator.curator == curator_id):
        products.add(product_curator.product)
    for product in products:
        orders = Shoplist.select().where((Shoplist.product == product.id) & (Shoplist.curator == curator_id))
        for order in orders:
            order.curator = get_least_loaded_curator_for_product(product.id, curator_id)
            order.save()
    # actually delete the curator that is being deleted
    ProductCurator.delete().where(ProductCurator.curator == curator_id).execute()
    Curator.delete().where(Curator.id == curator_id).execute()


def create_shoplist_record(user_id, product_id, price):
    user = get_user_by_tg_id(user_id)
    curator = get_least_loaded_curator_for_product(product_id)

    if curator:
        logging.info(f"Created shoplist record: user {user_id} bought product {product_id}; curator: {curator.id}")
        i = Shoplist(user=user.id, product=product_id, ts=datetime.datetime.now(), price=price, curator=curator.id)
    else:
        logging.info(f"Created shoplist record: user {user_id} bought product {product_id}")
        i = Shoplist(user=user.id, product=product_id, ts=datetime.datetime.now(), price=price)
    i.save()


def get_products_bought_by_user(user_id) -> List[Products]:
    return Products.select().join(Shoplist).join(Users).where(Users.id == user_id)


class Photo(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    tg_id = TextField()

    class Meta:
        table_name = "photo"
        order_by = ("id",)


def create_photo(name, tg_id):
    p = Photo(name=str.lower(name), tg_id=tg_id)
    p.save()


def get_photo_by_id(id) -> Union[Photo, None]:
    try:
        return Photo.select().where(Photo.id == id).get()
    except DoesNotExist:
        logging.warning(f"photo_id {id} doesn't exist in the database table")
        return None


def get_photo_by_name(name) -> Union[Photo, None]:
    try:
        return Photo.select().where(Photo.name == name).get()
    except DoesNotExist:
        logging.warning(f"photo_id {name} doesn't exist in the database table")
        return None


def get_photo_by_name_tg_id(name) -> Union[Photo, None]:
    try:
        return Photo.select().where(Photo.name == name).get().tg_id
    except DoesNotExist:
        logging.warning(f"photo_id {name} doesn't exist in the database table")
        return None


class Question(BaseModel):
    id = PrimaryKeyField()
    question_text = TextField(null=False)
    photo = TextField(null=True)

    class Meta:
        table_name = "question"
        order_by = ("id",)


class Answer(BaseModel):
    id = PrimaryKeyField()
    answer_text = TextField(null=False)

    class Meta:
        table_name = "answer"
        order_by = ("id",)


class QuestionAnswer(BaseModel):
    id = PrimaryKeyField()
    question = ForeignKeyField(Question, field="id")
    answer = ForeignKeyField(Answer, field="id")

    class Meta:
        table_name = "question_answer"
        order_by = ("id",)


def get_question_answers(question_id) -> List[QuestionAnswer]:
    question_answers = QuestionAnswer.select().where(QuestionAnswer.question == question_id)
    return question_answers


# def get_answers_for_question(question_id) -> List[Answer]:
#     return Answer.select().join(QuestionAnswer).join(Question).where(Question.id == question_id).get()


class Questionnaire(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    first_question = ForeignKeyField(Question, field="id")

    class Meta:
        table_name = "questionnaire"
        order_by = ("id",)


class QuestionnaireQuestionAnswer(BaseModel):
    id = PrimaryKeyField()
    questionnaire = ForeignKeyField(Questionnaire, field="id")
    question_answer = ForeignKeyField(QuestionAnswer, field="id")
    next_question = ForeignKeyField(Question, field="id", null=True)

    class Meta:
        table_name = "questionnaire_question_answer"
        order_by = ("id",)


def get_questionnaire_question_answer(question_answer_id) -> QuestionnaireQuestionAnswer:
    question_answers = (
        QuestionnaireQuestionAnswer.select()
            .where(QuestionnaireQuestionAnswer.question_answer == question_answer_id)
            .get()
    )
    return question_answers


class UserAnswer(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, field="id")
    questionnaire_question_answer = ForeignKeyField(QuestionnaireQuestionAnswer, field="id")
    ts = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "user_answer"
        order_by = ("id",)


def save_user_answer(user_id, questionnaire_question_answer_id):
    user_answer = UserAnswer(user=user_id, questionnaire_question_answer=questionnaire_question_answer_id)
    user_answer.save()


def get_user_answer_by_user(user_id) -> Union[List[UserAnswer], None]:
    try:
        return UserAnswer.select().where(UserAnswer.user == user_id)
    except DoesNotExist:
        logging.debug(f"Non-existing user answer was requested for user {user_id}")
        return None


class Video(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    tg_id = TextField()

    class Meta:
        table_name = "video"
        order_by = ("id",)


def create_video(name, tg_id):
    v = Video(name=str.lower(name), tg_id=tg_id)
    v.save()


def get_video_by_name(name) -> Union[Video, None]:
    try:
        return Video.select().where(Video.name == name).get()
    except DoesNotExist:
        logging.warning(f"video {name} doesn't exist in the database table")
        return None


class Audio(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    tg_id = TextField()

    class Meta:
        table_name = "audio"
        order_by = ("id",)


def create_audio(name, tg_id):
    v = Audio(name=str.lower(name), tg_id=tg_id)
    v.save()


def get_audio_by_name(name):
    try:
        return Audio.select().where(Audio.name == name).get().tg_id
    except DoesNotExist:
        logging.warning(f"Audio `{name}` doesn't exist in the database table")
        return None


class Animation(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    tg_id = TextField()

    class Meta:
        table_name = "animation"
        order_by = ("id",)


def create_gif(name, tg_id):
    a = Animation(name=str.lower(name), tg_id=tg_id)
    a.save()


def get_animation_by_name(name) -> Union[Animation, None]:
    try:
        return Animation.select().where(Animation.name == name).get()
    except DoesNotExist:
        logging.warning(f"animation `{name}` doesn't exist in the database table")
        return None


def get_animation_by_name_tg_id(name) -> Union[Animation, None]:
    try:
        return Animation.select().where(Animation.name == name).get().tg_id
    except DoesNotExist:
        logging.warning(f"animation `{name}` doesn't exist in the database table")
        return None


class Documents(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    tg_id = TextField()

    class Meta:
        table_name = "documents"
        order_by = ("id",)


def create_document(name, tg_id):
    a = Documents(name=str.lower(name), tg_id=tg_id)
    a.save()


def get_document_by_name(name) -> Union[Documents, None]:
    try:
        return Documents.select().where(Documents.name == name).get()
    except DoesNotExist:
        logging.warning(f"Documents `{name}` doesn't exist in the database table")
        return None


def get_document_by_name_tg_id(name) -> Union[Documents, None]:
    try:
        return Documents.select().where(Documents.name == name).get().tg_id
    except DoesNotExist:
        logging.warning(f"Documents `{name}` doesn't exist in the database table")
        return None


class UserLesson(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, field="id")
    product = ForeignKeyField(Products, field="id")
    lesson = ForeignKeyField(Lesson, field="id")
    ts = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "user_lesson"
        order_by = ("id", "ts")


def save_user_lesson(user_id, product_id, lesson_id):
    ul = UserLesson(user=user_id, product=product_id, lesson=lesson_id)
    ul.save()


def get_latest_lesson_id(user_id, product_id) -> Union[UserLesson, None]:
    try:
        return (
            UserLesson.select()
                .where((UserLesson.user == user_id) & (UserLesson.product == product_id))
                .order_by(UserLesson.ts.desc())
                .limit(1)
                .get()
        )
    except DoesNotExist:
        return None


# =====================Бесплатный интенсив==========================
class UsersFreeIntensive(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, unique=True)
    day = IntegerField(default=0)
    ts = DateTimeField(default=datetime.datetime.now)
    end_ts = DateTimeField(null=True)

    class Meta:
        table_name = "users_free_intensive"
        order_by = ("id", "ts")


# ==================== Функции для пользователей бесплатного интенсива ======================
def register_user_on_free_intensive(user_id):
    user = get_user_by_tg_id(user_id)
    try:
        row = UsersFreeIntensive(user=user.id)
        row.save()
    except (IntegrityError, InternalError):
        logging.warning(f"This user - {user.tg_id} already exists")


def get_user_for_free_intensive(tg_id):
    id = get_user_by_tg_id(tg_id).id
    try:
        user = UsersFreeIntensive.select().where(UsersFreeIntensive.user == id).get()
        return user
    except DoesNotExist:
        return None


def get_users_for_free_intensive():
    return UsersFreeIntensive.select().where(UsersFreeIntensive.day > 0, UsersFreeIntensive.day < 8)


def get_users_for_free_intensive_where_day(day):
    return UsersFreeIntensive.select().where(UsersFreeIntensive.day == day)


def get_users_do_not_starting_intensive():
    return UsersFreeIntensive.select().where(UsersFreeIntensive.day == 0)


def get_users_fre_intensive_not_buying_korset(day):
    return UsersFreeIntensive.select().where(
        UsersFreeIntensive.user.not_in(Shoplist.select(Shoplist.user).where(Shoplist.product == 10)),
        UsersFreeIntensive.day == day,
    )


# ==================== Уроки бесплатного интенсива ======================
class LessonsFreeIntensive(BaseModel):
    id = PrimaryKeyField()
    day = IntegerField()
    time = TextField()
    text_lesson = TextField()
    gif_text = TextField(null=True)
    photo_text = TextField(null=True)
    audio_text = TextField(null=True)

    class Meta:
        table_name = "lessons_for_free_intensive"


# ==================== Функции для уроков бесплатного интенсива ======================


def get_lessons_for_free_intensive():
    return LessonsFreeIntensive.select()


def get_lessons_for_free_intensive_where_lesson_text(lesson_text):
    return LessonsFreeIntensive.select().where(LessonsFreeIntensive.text_lesson == lesson_text)


def update_user_day_for_free(user):
    user.day = user.day + 1
    user.save()


# ==================== Пользователи вебинара ======================
class UsersFridayVebinar(BaseModel):
    id = PrimaryKeyField()
    user_id = ForeignKeyField(Users)
    ts = DateTimeField(default=datetime.datetime.now)
    time_vebinar = TextField()
    sended = BooleanField(default=False)

    class Meta:
        table_name = "users_friday_intensive"


# ==================== Функции для вебинара ======================
def get_users_friday_vebinar_all():
    return UsersFridayVebinar.select().where(UsersFridayVebinar.sended == False)


def get_users_friday_vebinar(time_vebinar):
    return UsersFridayVebinar.select().where(
        UsersFridayVebinar.sended == False, UsersFridayVebinar.time_vebinar == time_vebinar
    )


def change_sended_users_friday_vebinar(user_id):
    row = UsersFridayVebinar.select().where(UsersFridayVebinar.user_id == user_id).get()
    row.sended = True
    row.save()


def register_user_friday_vebinar(tg_id, time_vebinar):
    user = get_user_by_tg_id(tg_id)
    row = UsersFridayVebinar(user_id=user.id, time_vebinar=time_vebinar)
    row.save()


# ==================== Таблица для предупредения о вебинаре ======================


class MessageFridayVebinar(BaseModel):
    id = PrimaryKeyField()
    time = TextField()
    time_vebinar = TextField()
    message_text = TextField()
    gif_text = TextField(null=True)
    photo_text = TextField(null=True)
    audio_text = TextField(null=True)


# ==================== функции предупредения о вебинаре ======================
def get_all_message_friday_vebinar():
    return MessageFridayVebinar.select()


# ==================== Апрель старт ======================
class AprilStart(BaseModel):
    id = PrimaryKeyField()
    user_id = ForeignKeyField(Users)

    class Meta:
        table_name = 'april_start'


def get_users_april_start():
    return AprilStart.select()


def get_user_april_on_tg_id(tg_id):
    user = get_user_by_tg_id(tg_id)
    if user:
        try:
            return AprilStart.select().where(AprilStart.user_id == user.id).get()
        except DoesNotExist:
            return None
    else:
        return None


def register_user_april_start(tg_id):
    user = get_user_by_tg_id(tg_id)
    row = AprilStart(user_id=user.id)
    row.save()


def get_users_april_start():
    return Users.select().join(AprilStart)


# ==================== АВТОВОРОНКИ ======================
class AutoFunnels(BaseModel):
    """
    Модель автоворонки
    """
    id = PrimaryKeyField()
    name = TextField()
    start_on_week = IntegerField(null=True)
    start_on_day_month = IntegerField(null=True)
    fast_start = BooleanField(default=False)
    product_id = ForeignKeyField(Products, null=True)
    job_buy = TextField(null=True)
    job_not_buy = TextField(null=True)
    created_ts = DateTimeField(default=datetime.datetime.now())

    class Meta:
        table_name = 'auto_funnels'


def create_auto_funnels(name, start_on_week=None, start_on_day_month=None, fast_start=False, product_id=None,
                        job_buy=None, job_not_buy=None):
    row = AutoFunnels(name=name, start_on_week=start_on_week, start_on_day_month=start_on_day_month,
                      fast_start=fast_start, product_id=product_id, job_buy=job_buy, job_not_buy=job_not_buy)
    row.save()
    return row


def get_all_auto_funnels():
    return AutoFunnels.select()


def get_auto_funnel_by_id(id) -> AutoFunnels:
    return AutoFunnels.select().where(AutoFunnels.id == id).get()


def get_auto_funnel_by_name(name) -> AutoFunnels:
    return AutoFunnels.select().where(AutoFunnels.name == name).get()


def delete_auto_funnel_by_id(id):
    to_del = AutoFunnels.select().where(AutoFunnels.id == id).get()
    to_del.delete_instance()


class QuestionsTest(BaseModel):
    id = PrimaryKeyField()
    text = TextField()

    class Meta:
        table_name = 'question_test'


def get_all_question_without_question(question_id):
    return QuestionsTest.select().where(QuestionsTest.id != question_id)


def get_question_by_id(question_id):
    try:
        return QuestionsTest.select().where(QuestionsTest.id == question_id).get()
    except DoesNotExist:
        return None


def delete_question_test(question_id):
    question = QuestionsTest.select().where(QuestionsTest.id == question_id).get()
    question.delete_instance()


def get_all_questions():
    return QuestionsTest.select()


def create_question(text):
    qt_row = QuestionsTest(text=text)
    qt_row.save()
    return qt_row


class MessageAutoFunnels(BaseModel):
    """
    Модель сообщений автоворонки
    """
    id = PrimaryKeyField()
    auto_funnel_id = ForeignKeyField(AutoFunnels, on_delete='CASCADE')
    type_message = TextField()
    message_text = TextField(null=True)
    photo = TextField(null=True)
    gif = TextField(null=True)
    video = TextField(null=True)
    voice = TextField(null=True)
    video_note = TextField(null=True)
    document = TextField(null=True)
    audio = TextField(null=True)
    day = IntegerField(null=True)
    hour = IntegerField(null=True)
    minute = IntegerField(null=True)
    interval_msg_id = IntegerField(null=True)
    interval_second = IntegerField(null=True)
    interval_day = IntegerField(null=True)
    interval_hour = IntegerField(null=True)
    interval_minute = IntegerField(null=True)
    delete_hour = IntegerField(null=True)
    delete_day = IntegerField(null=True)
    delete_minute = IntegerField(null=True)
    delete_second = IntegerField(null=True)
    link = TextField(null=True)
    text_link = TextField(null=True)
    is_first = BooleanField(null=True)
    test = IntegerField(null=True)

    class Meta:
        table_name = 'message_auto_funnels'


def get_last_message_af(funnel_id):
    last_day_msgs = MessageAutoFunnels.select().where(MessageAutoFunnels.auto_funnel_id == funnel_id).order_by(
        -MessageAutoFunnels.day)

    last_msg = last_day_msgs[0]
    for msg in last_day_msgs:
        if last_msg.day < msg.day:
            last_msg = msg
        elif last_msg.day == msg.day:
            if last_msg.hour < msg.hour:
                last_msg = msg

    return last_msg


def get_message_af_by_id(msg_id):
    try:
        return MessageAutoFunnels.select().where(MessageAutoFunnels.id == int(msg_id)).get()
    except DoesNotExist:
        return None


def delete_message_af_by_id(msg_id):
    MessageAutoFunnels.delete().where(MessageAutoFunnels.id == msg_id).execute()

def get_messages_by_interval_msg(msg_id):
    try:
        return MessageAutoFunnels.select().where(MessageAutoFunnels.interval_msg_id == msg_id)
    except DoesNotExist:
        return None


def get_first_message_af_by_funnel_id(funnel_id):
    try:
        return MessageAutoFunnels.select().where(MessageAutoFunnels.auto_funnel_id == funnel_id,
                                                 MessageAutoFunnels.is_first == True).get()
    except DoesNotExist:
        return None


def get_messages_days_distinct(funnel_id):
    # TODO: Функция под вопросом
    return MessageAutoFunnels.select(MessageAutoFunnels.day.desc(nulls='FIRST')).order_by(
        MessageAutoFunnels.day).distinct().where(
        MessageAutoFunnels.type_message == 'content')


def get_all_content_messages_by_funnel_id(funnel_id):
    return MessageAutoFunnels.select().where(MessageAutoFunnels.type_message == 'content',
                                             MessageAutoFunnels.auto_funnel_id == funnel_id)


def get_all_system_messages_by_funnel_id(funnel_id):
    return MessageAutoFunnels.select().where(MessageAutoFunnels.type_message == 'system',
                                             MessageAutoFunnels.auto_funnel_id == funnel_id)


def get_first_message_by_funnel_id(funnel_id):
    try:
        return MessageAutoFunnels.select().where(MessageAutoFunnels.is_first == True,
                                                 MessageAutoFunnels.auto_funnel_id == funnel_id).get()
    except DoesNotExist:
        return None


def get_msgs_by_funnel_id_and_type(msg_type, funnel_id):
    return MessageAutoFunnels.select().where(MessageAutoFunnels.type_message == msg_type,
                                             MessageAutoFunnels.auto_funnel_id == funnel_id)


def get_msgs_by_funnel_id_and_type_without_interval(msg_type, funnel_id):
    return MessageAutoFunnels.select().where(MessageAutoFunnels.type_message == msg_type,
                                             MessageAutoFunnels.auto_funnel_id == funnel_id,
                                             MessageAutoFunnels.interval_msg_id.is_null())


def create_msg_af(funnel_id, type_message, message_text, photo, gif, video, voice, video_note, document, audio, day,
                  hour, minute, interval_msg_id, interval_day, interval_hour, interval_minute, interval_second,
                  delete_hour, delete_day, delete_minute, delete_second, link, text_link, is_first, test):
    row = MessageAutoFunnels(
        auto_funnel_id=funnel_id,
        type_message=type_message,
        message_text=message_text,
        photo=photo,
        gif=gif,
        video=video,
        voice=voice,
        video_note=video_note,
        document=document,
        audio=audio,
        day=day,
        hour=hour,
        minute=minute,
        interval_msg_id=interval_msg_id,
        interval_day=interval_day,
        interval_hour=interval_hour,
        interval_minute=interval_minute,
        interval_second=interval_second,
        delete_hour=delete_hour,
        delete_day=delete_day,
        delete_minute=delete_minute,
        delete_second=delete_second,
        link=link,
        text_link=text_link,
        is_first=is_first,
        test=test
    )
    row.save()
    return row


def save_new_message_af(message_id, message_text, photo, gif, video, voice, video_note, document, audio, day,
                        hour, minute, interval_msg_id, interval_day, interval_hour, interval_minute, interval_second,
                        delete_hour, delete_day, delete_minute, delete_second, link, text_link, test):
    message: MessageAutoFunnels = get_message_af_by_id(message_id)
    message.message_text = message_text
    message.photo = photo
    message.gif = gif
    message.video = video
    message.voice = voice
    message.video_note = video_note
    message.document = document
    message.audio = audio
    message.day = day
    message.hour = hour
    message.minute = minute
    message.interval_msg_id = interval_msg_id
    message.interval_day = interval_day
    message.interval_hour = interval_hour
    message.interval_minute = interval_minute
    message.interval_second = interval_second
    message.delete_hour = delete_hour
    message.delete_day = delete_day
    message.delete_minute = delete_minute
    message.delete_second = delete_second
    message.link = link
    message.text_link = text_link
    message.test = test
    message.save()
    return message


class UserAutoFunnels(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, on_delete='CASCADE')
    funnel = ForeignKeyField(AutoFunnels, on_delete='CASCADE')
    day = IntegerField()
    ts = DateTimeField(default=datetime.datetime.now(tz=UTC_TIME_ZONE))
    exit_ts = DateTimeField(null=True)

    class Meta:
        table_name = 'users_auto_funnels'


def get_statistics_funnel(month, year, day=None):
    funnels = get_all_auto_funnels()
    all_count = get_all_count_users_funnels()
    if day:
        data_text = f'Дата: {day}.{month}.{year}\n\n'
    else:
        data_text = f'Дата: {month}.{year}\n\n'

    text = f'{data_text}🔹Общее\nВсего пользователей: {all_count}\n'

    no_complete_users = get_all_complete_funnel(True)
    complete_users = get_all_complete_funnel(False)

    text += f'Стартовали: {no_complete_users}\n'
    text += f'Завершили: {complete_users}\n\n'
    text += '🔹Детально:\n'
    for funnel in funnels:
        if day:
            users = get_count_users_funnel_by_date(day, month, year, funnel.id)
        else:
            users = get_count_users_funnel_by_month(month, year, funnel.id)
        text += f'На {funnel.name} - {users}\n'

    return text


def get_all_count_users_funnels():
    return UserAutoFunnels.select(UserAutoFunnels.user).distinct().count()


def get_all_complete_funnel(is_null):
    return UserAutoFunnels.select().where(UserAutoFunnels.exit_ts.is_null(is_null)).count()


def get_count_users_funnel_by_date(day, month, year, funnel):
    return UserAutoFunnels.select().where(UserAutoFunnels.ts.year == year, UserAutoFunnels.ts.month == month,
                                          UserAutoFunnels.ts.day == day, UserAutoFunnels.funnel == funnel).count()


def get_count_users_funnel_by_month(month, year, funnel):
    return UserAutoFunnels.select().where(UserAutoFunnels.ts.year == year, UserAutoFunnels.ts.month == month,
                                          UserAutoFunnels.funnel == funnel).count()


def get_auto_funnels_segment(funnel_id):
    return Users.select().join(UserAutoFunnels).where(UserAutoFunnels.exit_ts.is_null(),
                                                      UserAutoFunnels.funnel == funnel_id)


def user_is_exists_in_funnel(chat_id, funnel_id):
    user = get_user_by_tg_id(chat_id)
    user_af = UserAutoFunnels.select().where(UserAutoFunnels.user == user.id, UserAutoFunnels.funnel == funnel_id,
                                             UserAutoFunnels.exit_ts.is_null(True))
    if user_af:
        return True
    else:
        return False


async def update_days_users_af():
    rows = UserAutoFunnels.select().where(UserAutoFunnels.exit_ts.is_null())
    for user in rows:
        next_day = user.day + 1
        if user.day == -1:
            next_day = 1

        user.day = next_day
        user.save()


def exit_user_funnel(user, funnel):
    try:
        row = UserAutoFunnels.select().where((UserAutoFunnels.user == user) & (UserAutoFunnels.exit_ts.is_null()) &
                                             (UserAutoFunnels.funnel == funnel)).get()
        print(row)
    except Exception as e:
        print(e)
        return
    row.exit_ts = datetime.datetime.now()
    row.save()


def get_users_af_by_funnel_id(funnel_id):
    return UserAutoFunnels.select().where(
        (UserAutoFunnels.funnel == funnel_id) & (UserAutoFunnels.exit_ts.is_null()))


def register_af_user(chat_id, funnel_id, day):
    user = get_user_by_tg_id(chat_id)
    row = UserAutoFunnels(user=user.id, funnel=funnel_id, day=day)
    row.save()
    return row


class AnswerTest(BaseModel):
    id = PrimaryKeyField()
    question = ForeignKeyField(QuestionsTest, on_delete='CASCADE')
    text = TextField()

    class Meta:
        table_name = 'answer_test'


def get_answers_question(question_id):
    return AnswerTest.select().where(AnswerTest.question == question_id)


def delete_answer(answer_id):
    answer = AnswerTest.select().where(AnswerTest.id == answer_id).get()
    answer.delete_instance()


def get_answers_by_id(answer_id):
    return AnswerTest.select().where(AnswerTest.id == answer_id).get()


def create_answer(question_id, text):
    at_row = AnswerTest(text=text, question=question_id)
    at_row.save()
    return at_row


class ResultsTest(BaseModel):
    id = PrimaryKeyField()
    answer = ForeignKeyField(AnswerTest, on_delete='CASCADE')
    result_text = TextField(null=True)
    photo = TextField(null=True)
    gif = TextField(null=True)
    video = TextField(null=True)
    voice = TextField(null=True)
    video_note = TextField(null=True)
    document = TextField(null=True)
    audio = TextField(null=True)
    link = TextField(null=True)
    text_link = TextField(null=True)
    test = ForeignKeyField(QuestionsTest, null=True, on_delete='CASCADE')

    class Meta:
        table_name = 'result_test'


def get_result_by_id(result_id):
    try:
        return ResultsTest.select().where(ResultsTest.id == result_id).get()
    except DoesNotExist:
        return None


def get_result_by_answer_id(answer_id):
    try:
        return ResultsTest.select().where(ResultsTest.answer == answer_id).get()
    except DoesNotExist:
        return None


def add_result_test(answer, result_text, photo, gif, video, voice, video_note, document, audio, link, text_link, test):
    rt_row = ResultsTest(
        answer=answer,
        result_text=result_text,
        photo=photo,
        gif=gif,
        video=video,
        voice=voice,
        video_note=video_note,
        document=document,
        audio=audio,
        link=link,
        text_link=text_link,
        test=test
    )
    rt_row.save()
    return rt_row


def save_new_result_test(message_id, result_text, photo, gif, video, voice, video_note, document, audio, link,
                         text_link, test):
    result = get_result_by_id(message_id)
    result.result_text = result_text
    result.photo = photo
    result.gif = gif
    result.video = video
    result.voice = voice
    result.video_note = video_note
    result.document = document
    result.audio = audio
    result.link = link
    result.text_link = text_link
    result.test = test
    result.save()
    return result


class UserResultsTest(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, on_delete='CASCADE')
    result = ForeignKeyField(ResultsTest, on_delete='CASCADE')
    ts = DateTimeField(default=datetime.datetime.now())

    class Meta:
        table_name = 'user_result_test'


def register_user_result_test(chat_id, result_id):
    user = get_user_by_tg_id(chat_id)
    if user:
        user = user.id
        user_rt = UserResultsTest(user=user, result=result_id)
        user_rt.save()
        return user_rt
    else:
        return None


class SystemMessage(BaseModel):
    id = PrimaryKeyField()
    trigger = TextField(unique=True)
    photo = TextField(null=True)
    text = TextField(null=True)
    link = TextField(null=True)


def create_system_message(trigger, photo, text, link):
    system_message = SystemMessage(trigger=trigger, photo=photo, text=text, link=link)
    system_message.save()


def edit_message_by_trigger(trigger, photo, text, link):
    system_message = SystemMessage.select().where(SystemMessage.trigger == trigger).get()
    system_message.photo = photo
    system_message.text = text
    system_message.link = link
    system_message.save()
    return system_message


def exists_system_message_by_trigger(trigger):
    try:
        return SystemMessage.select().where(SystemMessage.trigger == trigger).get()
    except DoesNotExist:
        return None


class PrivateClub(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    channel = TextField(null=True)
    private_chat = TextField(null=True)

    class Meta:
        table_name = 'private_club'


def delete_private_club_by_id(club_id):
    club = PrivateClub.select().where(PrivateClub.id == club_id).get()
    club.delete_instance()
    return True


def change_name_private_club(name, club_id):
    club = PrivateClub.select().where(PrivateClub.id == club_id).get()
    club.name = name
    club.save()
    return club


def change_chat_private_club(chat, club_id):
    club = PrivateClub.select().where(PrivateClub.id == club_id).get()
    club.private_chat = chat
    club.save()
    return club


def change_channel_private_club(channel, club_id):
    club = PrivateClub.select().where(PrivateClub.id == club_id).get()
    club.channel = channel
    club.save()
    return club


def get_private_club_by_id(club_id):
    return PrivateClub.select().where(PrivateClub.id == club_id).get()


def create_private_club(name):
    club = PrivateClub(name=name)
    club.save()
    return club


def get_all_private_club():
    return PrivateClub.select()


class PrivateClubRate(BaseModel):
    id = PrimaryKeyField()
    private_club = ForeignKeyField(PrivateClub, on_delete='CASCADE')
    name = TextField()
    description = TextField()
    type_media = TextField(null=True)
    media_id = TextField(null=True)
    period = IntegerField()  # В месяцах
    demo_period = IntegerField(null=True)  # В днях
    price = IntegerField()  # в рублях

    class Meta:
        table_name = 'private_club_rate'


def get_rate_by_id(rate_id):
    return PrivateClubRate.select().where(PrivateClubRate.id == rate_id).get()


def delete_rate_by_id(rate_id):
    rate = PrivateClubRate.select().where(PrivateClubRate.id == rate_id).get()
    rate.delete_instance()
    return rate


def create_rate_private_club(private_club, name, description, type_media, media_id, period, demo_period, price):
    rate = PrivateClubRate(
        private_club=private_club,
        name=name,
        description=description,
        type_media=type_media,
        media_id=media_id,
        period=period,
        demo_period=demo_period,
        price=price
    )
    rate.save()
    return rate


def change_any_field(rate_id, name=None, desc=None, type_media=None, media_id=None, period=None, demo_period=None,
                     price=None):
    rate = PrivateClubRate.select().where(PrivateClubRate.id == rate_id).get()
    if name:
        rate.name = name
    if desc:
        rate.description = desc
    if type_media:
        rate.type_media = type_media
    if media_id:
        rate.media_id = media_id
    if period:
        rate.period = period
    if demo_period:
        rate.demo_period = demo_period
    if price:
        rate.price = price

    rate.save()
    return rate


def get_rate_private_club(club_id):
    return PrivateClubRate.select().where(PrivateClubRate.private_club == club_id)


class PrivateClubCategories(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    private_club = ForeignKeyField(PrivateClub, on_delete='CASCADE')

    class Meta:
        table_name = 'categories_private_club'


def delete_category_by_id(cat_id):
    cat = PrivateClubCategories.select().where(PrivateClubCategories.id == cat_id).get()
    cat.delete_instance()


def change_name_category_by_id(cat_id, new_name):
    cat = PrivateClubCategories.select().where(PrivateClubCategories.id == cat_id).get()
    cat.name = new_name
    cat.save()
    return cat


def get_category_pr_cl_by_id(cat_id):
    return PrivateClubCategories.select().where(PrivateClubCategories.id == cat_id).get()


def get_all_categories_by_club_id(club_id):
    return PrivateClubCategories.select().where(PrivateClubCategories.private_club == club_id)


def create_private_club_category(name, club_id):
    category = PrivateClubCategories(name=name, private_club=club_id)
    category.save()
    return category


class MessagesPrivateClub(BaseModel):
    id = PrimaryKeyField()
    private_club = ForeignKeyField(PrivateClub, on_delete='CASCADE')
    type_message = TextField()
    category = ForeignKeyField(PrivateClubCategories, on_delete='CASCADE', null=True)
    text = TextField()
    day = IntegerField()
    hour = IntegerField()
    minute = IntegerField()

    class Meta:
        table_name = 'messages_private_club'


def get_count_messages_pr_cl_by_category(category_id):
    return MessagesPrivateClub.select().where(MessagesPrivateClub.category == category_id).count()


def get_max_day_message(club_id):
    return MessagesPrivateClub.select(fn.MAX(MessagesPrivateClub.day)).where(
        MessagesPrivateClub.private_club == club_id).scalar()


def get_msg_pr_cl_by_id(msg_id):
    return MessagesPrivateClub.select().where(MessagesPrivateClub.id == msg_id).get()


def delete_msg_pr_cl_by_id(msg_id):
    msg = MessagesPrivateClub.select().where(MessagesPrivateClub.id == msg_id).get()
    msg.delete_instance()


def get_day_messages(club_id, day):
    return MessagesPrivateClub.select().where(
        MessagesPrivateClub.private_club == club_id,
        MessagesPrivateClub.day == day
    )


def create_message_private_club(private_club, text, day, hour, minute, type_message, category):
    message = MessagesPrivateClub(
        private_club=private_club,
        type_message=type_message,
        text=text,
        day=day,
        hour=hour,
        minute=minute,
        category=category
    )
    message.save()
    return message


def edit_message_private_club(private_club, text, day, hour, minute, type_message, category, msg_id):
    msg: MessagesPrivateClub = MessagesPrivateClub.select().where(MessagesPrivateClub.id == msg_id).get()
    msg.private_club = private_club
    msg.text = text
    msg.day = day
    msg.hour = hour
    msg.minute = minute
    msg.type_message = type_message
    msg.category = category
    msg.save()
    return msg


class UsersPrivateClub(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, on_delete='CASCADE')
    rate = ForeignKeyField(PrivateClubRate, on_delete='CASCADE')
    day = IntegerField(default=0)
    start_day = DateTimeField(default=datetime.datetime.now())
    end_date = DateTimeField()

    class Meta:
        table_name = 'users_private_club'


async def update_days_users_pr_club():
    rows = UsersPrivateClub.select().where(UsersPrivateClub.end_date > datetime.datetime.now())
    for user in rows:
        next_day = user.day + 1
        user.day = next_day
        user.save()


def get_user_rate(user_id):
    user_rate = UsersPrivateClub.select().where(UsersPrivateClub.user == user_id,
                                                UsersPrivateClub.end_date > datetime.datetime.now())
    return user_rate


def add_user_pr_club(chat_id, rate_id, end_date):
    user = get_user_by_tg_id(chat_id)
    user = UsersPrivateClub(user=user.id, rate=rate_id, end_date=end_date)
    user.save()
    return user


def get_users_private_club_by_day(day):
    return UsersPrivateClub.select().where(UsersPrivateClub.day == day)


class Courses(BaseModel):
    id = PrimaryKeyField()
    name = TextField()

    class Meta:
        table_name = 'courses'


def create_course(name):
    course = Courses(name=name)
    course.save()
    return course


def get_course_by_id(course_id):
    return Courses.select().where(Courses.id == course_id).get()


class RatesCourse(BaseModel):
    id = PrimaryKeyField()
    course = ForeignKeyField(Courses)
    curator = ForeignKeyField(Curator, null=True)
    name = TextField()
    desc = TextField()
    media_id = TextField(null=True)
    media_type = TextField(null=True)
    price = IntegerField()
    installment = BooleanField()
    duration = IntegerField()
    close_duration = IntegerField()
    demo_duration = IntegerField()
    chat = TextField(null=True)
    channel = TextField(null=True)
    type_start = TextField()
    start = IntegerField(null=True)


def get_rate_course_by_id(rate_id):
    return RatesCourse.select().where(RatesCourse.id == rate_id).get()


def get_all_rates_by_course_id(course_id):
    return RatesCourse.select().where(RatesCourse.course == course_id)


def create_rate_course(course_id: object, curator: object, name: object, desc: object, media_id: object,
                       media_type: object, price: object, intallment: object, duration: object,
                       close_duration: object, demo_duration: object, chat: object, channel: object, type_start: object,
                       start: object) -> object:
    """

    :rtype: object
    """
    rate = RatesCourse(
        course=course_id,
        curator=curator,
        name=name,
        desc=desc,
        media_id=media_id,
        media_type=media_type,
        price=price,
        intallment=intallment,
        duration=duration,
        close_duration=close_duration,
        demo_duration=demo_duration,
        chat=chat,
        channel=channel,
        type_start=type_start,
        start=start
    )
    rate.save()
    return rate


# ==================== Сбор статистики ======================

def get_statistics_by_date(day, month, year):
    users = Users.select().where(Users.ts.day == day, Users.ts.month == month, Users.ts.year == year)

    users_answer = (
        UserAnswer.select(UserAnswer.user)
            .distinct()
            .where(UserAnswer.ts.day == day, UserAnswer.ts.month == month, UserAnswer.ts.year == year)
    )

    count_users_answer = 0
    count_buy_course_after_testing = 0
    for user in users_answer:
        count_users_answer += 1
        if Shoplist.select().where(
                Shoplist.user == user.user,
                Shoplist.product == 29,
                Shoplist.ts.day == day,
                Shoplist.ts.month == month,
                Shoplist.ts.year == year,
        ):
            count_buy_course_after_testing += 1

    users_free_intensive = UsersFreeIntensive.select().where(
        UsersFreeIntensive.ts.day == day, UsersFreeIntensive.ts.month == month, UsersFreeIntensive.ts.year == year
    )

    all_price = 0
    statistics_for_sale = "Статистика по продажам\n\n"
    products = Products.select().where(Products.is_deleted == False)
    for product in products:
        sale = Shoplist.select().where(
            Shoplist.ts.day == day, Shoplist.ts.month == month, Shoplist.ts.year == year, Shoplist.product == product.id
        )
        if len(sale):
            sale_price = 0
            for sal in sale:
                sale_price += sal.price
            statistics_for_sale += f"{product.name} купили {len(sale)} на ₽{sale_price}\n"
            all_price += sale_price
        else:
            statistics_for_sale += f"{product.name} купили {len(sale)} на ₽0\n"

    text = (
        f"🔹Новых пользователей {len(users)}\n"
        f"🔹Прошли входное тестирование {count_users_answer}\n"
        f"🔹Купили Я жива после входного тестирования {count_buy_course_after_testing}\n"
        f"🔹Записались на 5 шагов {len(users_free_intensive)} \n"
    )

    users_friday_vebinar_14 = UsersFridayVebinar.select().where(
        UsersFridayVebinar.ts.day == day,
        UsersFridayVebinar.ts.month == month,
        UsersFridayVebinar.ts.year == year,
        UsersFridayVebinar.time_vebinar == "14-00",
    )

    users_friday_vebinar_19 = UsersFridayVebinar.select().where(
        UsersFridayVebinar.ts.day == day,
        UsersFridayVebinar.ts.month == month,
        UsersFridayVebinar.ts.year == year,
        UsersFridayVebinar.time_vebinar == "19-00",
    )
    text += f"🔹Записались на пятничный вебинар на 14:00 - {len(users_friday_vebinar_14)} на 19:00 - {len(users_friday_vebinar_19)}\n\n"
    text += statistics_for_sale
    text += f"\n💰Денег в кассе = {all_price}"
    return text


def get_statistics_by_month(month, year):
    users = Users.select().where(Users.ts.month == month, Users.ts.year == year)

    users_answer = (
        UserAnswer.select(UserAnswer.user).distinct().where(UserAnswer.ts.month == month, UserAnswer.ts.year == year)
    )

    count_users_answer = 0
    count_buy_course_after_testing = 0
    for user in users_answer:
        count_users_answer += 1
        if Shoplist.select().where(
                Shoplist.user == user.user, Shoplist.product == 29, Shoplist.ts.month == month, Shoplist.ts.year == year
        ):
            count_buy_course_after_testing += 1

    users_free_intensive = UsersFreeIntensive.select().where(
        UsersFreeIntensive.ts.month == month, UsersFreeIntensive.ts.year == year
    )

    all_price = 0
    statistics_for_sale = "Статистика по продажам\n\n"
    products = Products.select().where(Products.is_deleted == False)
    for product in products:
        sale = Shoplist.select().where(
            Shoplist.ts.month == month, Shoplist.ts.year == year, Shoplist.product == product.id
        )
        if len(sale):
            sale_price = 0
            for sal in sale:
                sale_price += sal.price
            statistics_for_sale += f"{product.name} купили {len(sale)} на ₽{sale_price}\n"
            all_price += sale_price
        else:
            statistics_for_sale += f"{product.name} купили {len(sale)} на ₽0\n"

    text = (
        f"🔹Новых пользователей {len(users)}\n"
        f"🔹Прошли входное тестирование {count_users_answer}\n"
        f"🔹Купили Я жива после входного тестирования {count_buy_course_after_testing}\n"
        f"🔹Записались на 5 шагов {len(users_free_intensive)} \n"
    )
    users_friday_vebinar_14 = UsersFridayVebinar.select().where(
        UsersFridayVebinar.ts.month == month,
        UsersFridayVebinar.ts.year == year,
        UsersFridayVebinar.time_vebinar == "14-00",
    )

    users_friday_vebinar_19 = UsersFridayVebinar.select().where(
        UsersFridayVebinar.ts.month == month,
        UsersFridayVebinar.ts.year == year,
        UsersFridayVebinar.time_vebinar == "19-00",
    )
    text += f"🔹Записались на пятничный вебинар на 14:00 - {len(users_friday_vebinar_14)} на 19:00 - {len(users_friday_vebinar_19)}\n\n"
    text += statistics_for_sale
    text += f"\n💰Денег в кассе = {all_price}"
    return text



# main tables' initialization
for table_class in (
        Admins,
        Users,
        Categories,
        Products,
        Lesson,
        ProductLesson,
        Curator,
        ProductCurator,
        Shoplist,
        UserLesson,
        UsersFreeIntensive,
        LessonsFreeIntensive,
        UsersFridayVebinar,
        MessageFridayVebinar,
        AprilStart,
        Documents,
        AutoFunnels,
        MessageAutoFunnels,
        UserAutoFunnels,
        QuestionsTest,
        AnswerTest,
        ResultsTest,
        UserResultsTest,
        SystemMessage,
        PrivateClub,
        PrivateClubRate,
        PrivateClubCategories,
        MessagesPrivateClub,
        UsersPrivateClub,
        Courses,
        RatesCourse
):
    table_class.create_table()

db_handler.execute_sql(
    """
create or replace view curator_load as
(
    with c as (
        select pc.product_id, c.id, username, 0 as load
        from curator c
        join product_curator pc on c.id = pc.curator_id
    ),
    l as (
        select pc.product_id, c.id, username, count(*) as load
        from curator c
        join product_curator pc on c.id = pc.curator_id
        join shoplist s on c.id = s.curator_id
        group by pc.product_id, c.id
        order by load
    )
    select c.id as curator_id, c.product_id, coalesce(c.load + l.load, 0) as load
    from c left join l on c.id = l.id and c.product_id = l.product_id
);
"""
)

# questionnaire tables' initialization
for table_class in (
        Photo,
        Question,
        Answer,
        QuestionAnswer,
        Questionnaire,
        QuestionnaireQuestionAnswer,
        UserAnswer,
        Audio,
):
    table_class.create_table()

# video tables' initialization
Video.create_table()
Animation.create_table()

def fill_table(table_class: Type[BaseModel], inputs: List[Dict]):
    # insert only in an empty table
    if not table_class.select():
        for record in inputs:
            table_class.create(**record)
    else:
        logging.info(f"table {table_class.__name__} already has records, the insertion of new rows is skipped!")

