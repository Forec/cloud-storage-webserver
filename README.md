# ������ Web ������

[![License](http://7xktmz.com1.z0.glb.clouddn.com/license-UDL.svg)](https://github.com/Forec/cloud-storage-webserver/blob/master/LICENSE) 
[![Build Status](https://travis-ci.org/Forec/cloud-storage-webserver.png)](https://travis-ci.org/Forec/cloud-storage-webserver) 
[![Doc](http://7xktmz.com1.z0.glb.clouddn.com/docs-icon.svg)](http://cloud-storage-webserver.readthedocs.io/zh_CN/latest/)

[**������**](http://cloud.forec.cn) ���� 2016 ���һ��γ����ѡ�⣬Ŀ������У԰����������Ƽ��ס������С��ģ�ƴ洢���񡣶����ƵĽṹ��ʵ�ַǳ��򵥣��������ڰ�����ݮ�����ڵ��κμ�����ϣ�Ŀǰ�ҽ��䲿�����ҵ���ݮ�ɺ�һ̨�Ʒ������ϡ��Ҷ���ݮ�ɵĶ�Ӧ�˿����� NAT ��͸����˼�ʹ��У��Ҳ���Է��ʴ洢�ڶ����Ƶ��ļ���У����Ϊ�����ƵĴ����ṩ�˷ǳ��õ������������������ʹ����������� Windows 7 ϵͳ�£�IPv4Э�飩�������Ƶ� [�ͻ���](https://github.com/forec-org/cloud-storage-client)�ɴﵽ 42 MB/s �������ٶȡ�

�˲ֿ��й��˶����Ƶ� Web ������Դ�룬�����ͨ���κ��豸����������ʶ����ơ���Ϊ˽��ǩ���֤�鲻����������Σ����Բ���ʱ����ʹ�� https Э�顣�ڹ�������Ķ����Ʒ���������չʾ�ã����ṩ����ע����κ�ʵ�ʹ��ܣ��������ʹ�ò����û���¼���顣�����ϲ������ϣ��ʹ��ʹ�ö����ƣ��� [Email](mailto:forec.edu.cn) �ң��һ�Ϊ���ں�̨����һ����ʹ�õ��˻���

�����Ƶ�Ӧ�ó���������й��ڲֿ� [������ Ӧ�÷�����](https://github.com/Forec/cloud-storage) �У�ʹ�� Golang ��д��

## �������ĵ�

���������µĿ������ĵ����� [�˴�](http://cloud-storage-webserver.readthedocs.io/zh_CN/latest/) �鿴��

## ����

������ Web ������ʹ�� Flask ��ܣ������� Flask ����Ϥ�����Ժܿ��˽ⶥ���ƵĽṹ��

������Ŀ¼�ṹ����������ʾ��

```
cloud-storage-web
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
