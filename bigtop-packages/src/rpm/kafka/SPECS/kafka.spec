# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define kafka_name kafka
%define lib_kafka /usr/lib/%{kafka_name}
%define etc_kafka /etc/%{kafka_name}
%define config_kafka %{etc_kafka}/conf
%define log_kafka /var/log/%{kafka_name}
%define bin_kafka /usr/bin
%define man_dir /usr/share/man

%if  %{?suse_version:1}0
%define doc_kafka %{_docdir}/kafka
%define alternatives_cmd update-alternatives
%else
%define doc_kafka %{_docdir}/kafka-%{kafka_version}
%define alternatives_cmd alternatives
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: kafka
Version: %{kafka_version}
Release: %{kafka_release}
Summary: A high-throughput distributed messaging system.
URL: http://kafka.apache.org
Group: Development/Libraries
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: ASL 2.0 
Source0: %{name}-%{kafka_base_version}.tgz
Source1: do-component-build 
Source2: install_%{name}.sh
Requires: bigtop-utils


%description 
Kafka is a high-throughput distributed messaging system.
    
%prep
%setup

%build
bash $RPM_SOURCE_DIR/do-component-build

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_kafka.sh \
          --build-dir=`pwd`         \
          --prefix=$RPM_BUILD_ROOT

%post
%{alternatives_cmd} --install %{config_kafka} %{kafka_name}-conf %{config_kafka}.dist 30

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{kafka_name}-conf %{config_kafka}.dist || :
fi

#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,root,root,755)
%config(noreplace) %{config_kafka}.dist
%doc %{doc_kafka}
%{lib_kafka}
%{bin_kafka}/startkafka
