from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EmployeeRole(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=100,choices=(('Frontend Developer','Frontend Developer'),('Backend Developer','Backend Developer'),('Full Stack Developer','Full Stack Developer'),('Project Manager','Project Manager'),('Team Lead','Team Lead'),('digital marketing','digital marketing'),('graphic designer','graphic designer'),('UI/UX Designer','UI/UX Designer'),('Content Writer','Content Writer'),('Video Editor','Video Editor'),('Social Media Manager','Social Media Manager')))
    # role=models.CharField(max_length=100)
                                                                                            
    def __str__(self):
        return self.role

class EmployeeLeave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    total_days = models.PositiveIntegerField(editable=False)
    leavestatus = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.leave_start_date and self.leave_end_date:
            self.total_days = (self.leave_end_date - self.leave_start_date).days + 1    
        super().save(*args, **kwargs)
    
class EmployeeSalary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.salary}"
    
class EmployeeAttandence(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    checkin=models.TimeField()
    checkout=models.TimeField()
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    work_duration = models.DurationField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"