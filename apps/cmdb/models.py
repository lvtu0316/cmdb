from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords


User = get_user_model()
# Create your models here.


class TimeAbstract(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class DeviceAbstract(models.Model):
    """
    设备基本信息
    """
    STATUS_CHOICES =(
        ("using", "使用中"),
        ("stopping", "已停用"),
        ("repairing", "维修中"),
        ("reserve", "备用"),
        ("dumping", "报废")
    )
    name = models.CharField(max_length=100, verbose_name='名称')
    brand = models.CharField(max_length=50, blank=True, verbose_name='品牌')
    device_model = models.CharField(max_length=150, blank=True, default='', verbose_name='设备型号')
    supplier = models.CharField(max_length=30, blank=True, verbose_name="供应商")
    status = models.CharField(max_length=10, blank=True, choices=STATUS_CHOICES, default='using', verbose_name='状态')
    position = models.CharField(max_length=150, blank=True, default='', verbose_name='位置')
    use_department = models.CharField(max_length=50, blank=True, verbose_name='使用部门')
    leader = models.CharField(max_length=50, blank=True, verbose_name='责任人')
    leader_phone = models.CharField(max_length=50, blank=True, verbose_name='责任人联系方式')
    ops_department = models.CharField(max_length=50, blank=True, verbose_name='运维部门')
    ops_leader = models.CharField(max_length=50, blank=True, verbose_name='运维责任人')
    ops_leader_phone = models.CharField(max_length=11, blank=True, verbose_name='运维联系方式')
    online_date = models.DateField(null=True, blank=True, default='', verbose_name="上架日期")
    offline_date = models.DateField(null=True, blank=True, default='', verbose_name="下架日期")

    warranty_date = models.DateField(verbose_name="维保截止日期")
    remarks = models.TextField(blank=True, verbose_name="备注")

    class Meta:
        abstract = True


class Business(TimeAbstract):

    NETWORK_CHOICES = (
        ('gongan', '公安网'),
        ('internet', '互联网')
    )
    name = models.CharField(max_length=50, verbose_name='业务名称')
    use = models.CharField(max_length=50, blank=True, verbose_name='用途')
    network = models.CharField(max_length=20, blank=True, choices=NETWORK_CHOICES, default='gongan', verbose_name='所属网络')
    login_url = models.CharField(max_length=50, blank=True, verbose_name='登录方式')
    username = models.CharField(max_length=50, blank=True, verbose_name='用户名')
    password = models.CharField(max_length=50, blank=True, verbose_name='密码')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父业务")

    class Meta:
        verbose_name = '业务'
        verbose_name_plural = verbose_name


class DeviceGroup(TimeAbstract):
    name = models.CharField(max_length=50, verbose_name='分组名称')
    desc = models.CharField(max_length=150, blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '设备分组'
        verbose_name_plural = verbose_name


class Label(TimeAbstract):
    name = models.CharField(max_length=50, verbose_name='标签名称')
    desc = models.CharField(max_length=150, blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Cabinet(TimeAbstract):
    """
    机柜
    """
    num = models.CharField(max_length=50, verbose_name='机柜编号')
    brand = models.CharField(max_length=30, blank=True, verbose_name='品牌')
    location = models.CharField(max_length=30, blank=True, verbose_name='位置')


class Host(TimeAbstract, DeviceAbstract):
    '''
    主机信息表
    '''

    HOST_TYPE_CHOICE = (
        ("virtual", "虚拟机"),
        ("physical", "物理机"),
        ("other", "其他")
    )
    NETWORK_TYPE_CHOICE = (
        ("gongan", "公安网"),
        ("internet", "互联网"),
        ("shipin", "视频专网")
    )
    OS_TYPE_CHOICE = (
        ("linux", "Linux"),
        ("windows", "windows"),
        ("other", "其他")
    )
    hostname = models.CharField(max_length=50, blank=True, verbose_name='主机名')
    ip = models.CharField(max_length=20, unique=True, verbose_name='IP')
    manager_ip = models.CharField(max_length=20, blank=True, verbose_name='管理IP')
    sn = models.CharField(max_length=150, blank=True, default='', verbose_name='SN号码')
    device_type = models.CharField(max_length=20, choices=HOST_TYPE_CHOICE, blank=True, null=True, default='', verbose_name='设备类型')
    network_type = models.CharField(max_length=20, blank=True, null=True, choices=NETWORK_TYPE_CHOICE, default='', verbose_name='网络类型')
    changed_by = models.ForeignKey(User, null=True, blank=True,  on_delete=models.SET_NULL)
    businesses = models.ManyToManyField("Business", blank=True, verbose_name="业务")
    groups = models.ManyToManyField("DeviceGroup", blank=True, verbose_name="设备组")
    labels = models.ManyToManyField("Label", blank=True, verbose_name="标签")
    cabinet = models.ForeignKey("Cabinet", blank=True, null=True, on_delete=models.SET_NULL, verbose_name="机柜")
    history = HistoricalRecords(excluded_fields=['add_time', 'modify_time', 'pid'])
    username = models.CharField(max_length=20, blank=True, verbose_name='用户')
    password = models.CharField(max_length=50, blank=True, verbose_name='密码')

    os_type = models.CharField(max_length=10, blank=True,null=True, choices=OS_TYPE_CHOICE, verbose_name='操作系统类型')
    os_version = models.CharField(max_length=50, blank=True, verbose_name='操作系统版本')

    cpu_model = models.CharField(max_length=50, blank=True, verbose_name='CPU型号')
    cpu_number = models.IntegerField(blank=True, null=True, verbose_name='CPU颗数')
    cpu_core = models.IntegerField(blank=True, null=True, verbose_name='CPU核数')

    memory_model = models.CharField(max_length=50, blank=True, verbose_name='内存卡型号')
    memory_brand = models.CharField(max_length=50, blank=True, verbose_name='内存卡品牌')
    memory_num = models.IntegerField(null=True, blank=True, verbose_name='内存卡条数')
    memory_size = models.IntegerField(null=True, blank=True, verbose_name='内存大小')

    disk_size = models.IntegerField(null=True, blank=True, verbose_name='硬盘大小')
    disk_num = models.IntegerField(null=True, blank=True, verbose_name='硬盘个数')

    net_card_info = models.CharField(max_length=50, blank=True, verbose_name='网卡信息')

    file = models.FileField(upload_to="uploads/hosts/%Y-%m-%d", null=True, blank=True, verbose_name="附件")

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name


