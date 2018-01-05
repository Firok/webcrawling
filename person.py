import json


class Person:
    def __init__(self, photo, name, job_title, email, ext, fax, phone, work_allocation=None):
        self.photo = photo
        self.name = name
        self.job_title = job_title
        self.email = email
        self.ext = ext
        self.fax = fax
        self.phone = phone
        self.work_allocation = work_allocation

    def to_json(self):
        """
        Serialize the object person
        """
        return json.dumps(self, default=lambda p: p.__dict__,indent=4)
