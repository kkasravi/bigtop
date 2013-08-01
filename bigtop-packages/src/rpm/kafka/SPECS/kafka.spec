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
%define run_kafka /var/run/%{kafka_name}
%define bin_kafka /usr/bin
%define man_dir /usr/share/man

%if  %{?suse_version:1}0
%define doc_kafka %{_docdir}/kafka
%define alternatives_cmd update-alternatives
%define alternatives_dep update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%else
%define doc_kafka %{_docdir}/kafka-%{kafka_version}
%define alternatives_cmd alternatives
%define alternatives_dep chkconfig
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: kafka
Version: %{kafka_version}
Release: %{kafka_release}
Summary: A high-throughput distributed messaging system.
URL: http://kafka.apache.org
Group: Development/Libraries
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: APL2
Source0: %{name}-%{kafka_base_version}.tgz
Source1: do-component-build 
Source2: install_%{name}.sh
BuildArch: noarch
BuildRequires: autoconf, automake
Requires(pre): coreutils, /usr/sbin/groupadd, /usr/sbin/useradd
Requires(post): %{alternatives_dep}
Requires(preun): %{alternatives_dep}
Requires: bigtop-utils >= 0.6
%if  %{?suse_version:1}0
# Required for init scripts
Requires: insserv
%endif

%if  0%{?mgaversion}
# Required for init scripts
Requires: initscripts
%endif

%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: redhat-lsb
%endif

%description 
Kafka is a high-throughput distributed messaging system.
    
%prep
%setup -n %{name}-%{kafka_base_version}-src

%build
bash $RPM_SOURCE_DIR/do-component-build

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_kafka.sh \
          --build-dir=`pwd`         \
          --prefix=$RPM_BUILD_ROOT
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/
init_file=$RPM_BUILD_ROOT/%{initd_dir}/%{name}
%__cp $orig_init_file $init_file
chmod 755 $init_file

%pre
getent group kafka >/dev/null || groupadd -r kafka
getent passwd kafka > /dev/null || useradd -c "Kafka" -s /sbin/nologin -g kafka -r -d %{lib_kafka} kafka 2> /dev/null || :

%__install -d -o kafka -g kafka -m 0755 %{run_kafka}
%__install -d -o kafka -g kafka -m 0755 %{log_kafka}
%__install -d -o kafka -g kafka -m 0755 %{lib_kafka}

%post
%{alternatives_cmd} --install %{config_kafka} %{kafka_name}-conf %{config_kafka}.dist 30
chkconfig --add %{name}

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
%{config_kafka}
%{config_kafka}ig
%{lib_kafka}/bin/*
%{lib_kafka}/*.jar
%{lib_kafka}/config
%{bin_kafka}/kafka
