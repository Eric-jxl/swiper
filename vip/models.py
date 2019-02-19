from django.db import models


class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=16, unique=True, verbose_name='名称')
    level = models.IntegerField(default=0, unique=True, verbose_name='会员等级')
    price = models.FloatField(verbose_name='价格')

    def perms(self):
        '''Vip 具有的所有权限'''
        # 取出所有对应的关系
        relations = VipPermRelation.objects.filter(vip_id=self.id).only('perm_id')

        # 取出对应的权限模型
        perm_id_list = [rel.perm_id for rel in relations]
        return Permission.objects.filter(id__in=perm_id_list)

    def has_perm(self, perm_name):
        '''检查是否具有某权限'''
        for perm in self.perms():
            if perm.name == perm_name:
                return True
        return False


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=16, unique=True, verbose_name='名称')
    description = models.TextField(verbose_name='描述')


class VipPermRelation(models.Model):
    '''VIP-权限 关系表'''
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
