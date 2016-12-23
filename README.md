# ������ Web ������

[![License](http://7xktmz.com1.z0.glb.clouddn.com/license-UDL.svg)](https://github.com/Forec/zenith-cloud/blob/master/LICENSE) 
[![Build Status](https://travis-ci.org/Forec/zenith-cloud.png)](https://travis-ci.org/Forec/zenith-cloud) 
[![Documentation Status](https://readthedocs.org/projects/zenith-cloud/badge/?version=latest)](http://zenith-cloud.readthedocs.io/zh_CN/latest/?badge=latest)

[**������**](http://cloud.forec.cn) ���� 2016 ���һ��γ����ѡ�⣬Ŀ������У԰����������Ƽ��ס������С��ģ�ƴ洢���񡣶����ƵĽṹ��ʵ�ַǳ��򵥣��������ڰ�����ݮ�����ڵ��κμ�����ϣ�Ŀǰ�ҽ��䲿�����ҵ���ݮ�ɺ�һ̨�Ʒ������ϡ��Ҷ���ݮ�ɵĶ�Ӧ�˿����� NAT ��͸����˼�ʹ��У��Ҳ���Է��ʴ洢�ڶ����Ƶ��ļ���У����Ϊ�����ƵĴ����ṩ�˷ǳ��õ������������������ʹ����������� Windows 7 ϵͳ�£�IPv4Э�飩�������Ƶ� [�ͻ���](https://github.com/forec-org/cloud-storage-client)�ɴﵽ 42 MB/s �������ٶȡ�

�˲ֿ��й��˶����Ƶ�Ӧ�ó���������� Web ������Դ�룬�����ͨ�� [non1996](https://github.com/non1996) ��д�� [�ͻ���](https://github.com/forec-org/cloud-storage-client) ��ȡ������Ӧ�ó��������֧�֣�Ҳ����ʹ���κ��豸����������ʶ����� Web ����������Ϊ˽��ǩ���֤�鲻����������Σ����Զ����Ƶ� Web ����������ʱ����ʹ�� https Э�顣�ڹ�������Ķ����Ʒ���������չʾ�ã����ṩ����ע����κ�ʵ�ʹ��ܣ��������ʹ�ò����û���¼���顣�����ϲ������ϣ��ʹ��ʹ�ö����ƣ��� [Email](mailto:forec.edu.cn) �ң��һ�Ϊ���ں�̨����һ����ʹ�õ��˻���

## �������ĵ�

���������µĿ������ĵ����� [�˴�](http://zenith-cloud.readthedocs.io/zh_CN/latest/) �鿴��

## ����

������ Web ������ʹ�� Flask ��ܣ������� Flask ����Ϥ�����Ժܿ��˽ⶥ���� Web �������Ľṹ��������Ӧ�ó��������ʹ�� Golang ��д��

������ȫ��Դ��Ŀ¼�ṹ����������ʾ��

```
zenith-cloud
 - app
   - cstruct
     - cuser.go
     - cuser_operations.go
     - cuser_transmissions.go
     - ...
   - cloud
   - server
   - client
   - authenticate
   - transmit
   - config
 - web
   - app
     - auth
     - main
     - static
       - thumbnail
     - templates
     - ...
     - models.py
   - settings
   - config.py
   - manage.py
   - work.db
```

���½��ܶ������������漰�Ĺؼ������ļ���
* `config.py`�������� Web ��������ȫ�����ã������ļ�ʵ��洢��λ�á����ݿ�·����·���ָ���������Ա����ȣ�ÿ�����ú���ж�Ӧ��ע��˵������ϸ���ÿɲ鿴 [������ȫ�������ļ�](#)��
* `manage.py`�������� Web ������ͨ�� `manage.py` ע����������չ�����ļ��ṩ�˼����򵥵����������ݿ��ʼ���������û���ʼ����shell�����ȡ���ϸ����ɲ鿴 [�����ƿ����ļ�](#)��
* `work.db`�������ƴ洢�û���Ϣ�����ݿ⣬Ĭ��ʹ�� SQLITE�������ͨ���޸� `config.py` ���������ݿ����ͺ�·���������޸ķ����ɲ鿴 [���������ݿ�����](#)��
* `settings` Ŀ¼����Ŀ¼������һ�� Ngrok �����ļ��ͼ����������ļ������ڲ�������������Ʒ��������������÷����ɲ鿴 [�����Ʋ���](#)��

�����Ʒ�������ͨ�����·�ʽ���𣨲���ǰ��ȷ����������������� Python3 ·������
```shell
git clone https://github.com/Forec/cloud-storage-webserver.git
cd cloud-storage-webserver/settings
./setup.sh		# Windows ϵͳ˫��ִ�� setup.bat
```

## ����
�����Ʒ�������ͨ�����·�ʽ��������ȷ������ǰ�ѳɹ����𣩡������������ʽ�Ͳ�����鿴 [���������в�������](#)��
```
cd /path/to/cloud-storage-webserver/settings
./run.sh		# Windows ϵͳ˫��ִ�� run.bat
```

# ���֤
�˲ֿ��е�ȫ��������ֿܲ��� [License](https://github.com/Forec/cloud-storage-webserver/blob/master/LICENSE) ���������֤������
