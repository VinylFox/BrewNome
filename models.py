import sqlobject as db

db.sqlhub.processConnection = db.connectionForURI("mysql://brewnome:br3wl0v3r@localhost/brewnome")

class TaskQueueGroup(db.SQLObject):
    queue_name = db.StringCol(length=64)
    queue_interval = db.IntCol(default=1)

class TaskQueue(db.SQLObject):
    task_group = db.ForeignKey("TaskQueueGroup", cascade=False)
    task_url = db.StringCol(length=255)
    task_data = db.StringCol()
    task_time = db.TimestampCol()

class Summary(db.SQLObject):
    summary_category = db.StringCol(length=64)
    summary_type = db.StringCol(length=64)
    summary_value = db.StringCol(length=64)
    summary_result = db.StringCol(length=64)

class VehicleMake(db.SQLObject):
    make_code = db.StringCol(length=5)
    make_description = db.StringCol(length=128)
    total_make = db.IntCol()
    total_make_fine_amt = db.CurrencyCol()
