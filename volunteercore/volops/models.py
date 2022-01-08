from datetime import datetime
from volunteercore import db
from volunteercore.mixins import PagininatedAPIMixin
import flask_whooshalchemyplus

tags = db.Table(
    'tags',
    db.Column('opportunity_id', db.Integer, db.ForeignKey('opportunity.id')),
    db.Column('tags_id', db.Integer, db.ForeignKey('tag.id'))
)


class Opportunity(PagininatedAPIMixin, db.Model):
    __tablename__ = 'opportunity'
    __searchable__ = ['tags_string']

    id = db.Column(db.Integer(), primary_key=True, index=True)
    active = db.Column(db.Boolean())
    name = db.Column(db.String(100), index=True)
    description = db.Column(db.Text())
    shift_hours = db.Column(db.Float())
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    volunteers_needed = db.Column(db.Integer())
    tags_string = db.Column(db.String(200))

    # Many to many relations
    tags = db.relationship(
        'Tag', secondary='tags', lazy='subquery',
        backref=db.backref('opportunities', lazy=True))

    #TODO actually check what this does
    def get_tags(self, categorized=True):
        if self.tags:
            if categorized:
                tag_categories = []
                for category in TagCategory.query.all():
                    tag_categories.append(category.name)
                tag_data = {}
                for category in tag_categories:
                    tags = []
                    for tag in TagCategory.query.filter_by(
                            name=category).first().tags:
                        if tag in self.tags:
                            tags.append(tag.name)
                    if tags:
                        tag_data[category] = tags
            else:
                tag_data = []
                for tag in self.tags:
                    tag_data.append(tag.name)
            return tag_data
        else:
            return None

    def update_tag_strings(self):
        tags_string_total = ""
        for tag in self.tags:
            tags_string_total = tags_string_total + tag.name + " "
        self.tags_string = tags_string_total

    def to_dict(self):
        data = {
            'id': self.id,
            'active': self.active,
            'name': self.name,
            'description': self.description,
            'shift_hours': self.shift_hours,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'volunteers_needed': self.volunteers_needed,
            'tag_count': len(self.tags),
        }
        if self.tags:
            data['tags'] = self.get_tags()
        return data

    def from_dict(self, data, new_opportunity=False):
        field_names = [
            'name', 'active', 'description', 'shift_hours',
            'start_date', 'end_date', 'volunteers_needed',
            'tag_count', 
        ]
        for field in field_names:
            if field in data:
                setattr(self, field, data[field])
        for field in ['start_date', 'end_date']:
            if field in data:
                setattr(self, field, datetime.strptime(data[field],
                        '%Y%m%d').date())
        if 'tags' in data:
            tag_ids = []
            for tag in data['tags']:
                tag_ids.append(Tag.query.filter_by(name=tag).first())
            setattr(self, 'tags', tag_ids)

    def __repr__(self):
        return '<Opportunity {}>'.format(self.name)


class TagCategory(PagininatedAPIMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(60), index=True, unique=True)
    tags = db.relationship('Tag', backref='tag_category', lazy='dynamic')

    def to_dict(self):
        tags = []
        for tag in self.tags:
            tags.append(tag.name)
        data = {
            'id': self.id,
            'category_name': self.name,
            'tags': tags
            }
        return data

    def from_dict(self, data, new_tag_category=False):
        if 'category_name' in data:
            setattr(self, 'name', data['category_name'])
        if 'tags' in data:
            tag_ids = []
            for tag in data['tags']:
                tag_ids.append(Tag.query.filter_by(name=tag).first())
            setattr(self, 'tags', tag_ids)

    def __repr__(self):
        return '<Tag Category {}>'.format(self.name)


class Tag(PagininatedAPIMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(60), index=True, unique=False)
    tag_category_id = db.Column(db.Integer, db.ForeignKey('tag_category.id'))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'tag_category': TagCategory.query.filter_by(
                id=self.tag_category_id).first().name
        }
        return data

    def from_dict(self, data, new_tag=False):
        if 'name' in data:
            setattr(self, 'name', data['name'])
        if 'tag_category' in data:
            tag_category_id = TagCategory.query.filter_by(
                name=data['tag_category']).first().id
            setattr(self, 'tag_category_id', tag_category_id)

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

class Hours(PagininatedAPIMixin, db.Model):

    id = db.Column(db.Integer(), primary_key=True, index=True)
    user_id = db.Column(db.Integer())
    hours = db.Column(db.Float())
    description = db.Column(db.Text())
    #We expect a value in the format YYYY-MM
    datetime = db.Column(db.Text)

    def to_dict(self):
        data = {
            "user_id":self.user_id,
            "hours":self.hours,
            "datetime":self.datetime,
            "description":self.description,
        }
        return data
    
    def from_dict(self, data):
        field_names = [
            'hours','datetime','user_id','description',
        ]
        for field in field_names:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<Hours {}>'.format(self.id)
