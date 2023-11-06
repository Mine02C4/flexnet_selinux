# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R -i /usr/local/bin/lmgrd; \
restorecon -R -i /usr/local/bin/lmutil; \
restorecon -R -i /usr/local/lib/flexnet; \
restorecon -R -i /usr/local/etc/flexnet; \

%define selinux_policyver 38.1.11-2

Name:   flexnet_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for FlexNet

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/Mine02C4/flexnet_selinux
Source0:	flexnet.pp
Source1:	flexnet.if
Source2:	flexnet_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for FlexNet.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/flexnet_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/flexnet.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r flexnet
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/flexnet.pp
%{_datadir}/selinux/devel/include/contrib/flexnet.if
%{_mandir}/man8/flexnet_selinux.8.*


%changelog
* Wed Oct 11 2023 NIWA Naoya <mine@mine02c4.nagoya> 1.0-1
- Initial version

