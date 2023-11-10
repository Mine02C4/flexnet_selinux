# SELinux policy module for FlexNet

**!IMPORTANT! : This is unofficial software; it is a policy created by an ordinary user independent of FlexNet's vendor.**

Installing this policy allows FlexNet to work under SELinux Enforcing environment. The policy restricts FlexNet's behavior whenever possible and mitigates security threats.

## Requirements

- Distribution : Rocky Linux 9
- FlexNet : v11.17.2.0

I believe it works in other environments as well. I would like information on confirmation that it works.

## Installation

### Step. -1 : Avoid ELF interpreter problem

Please perform the following workaround as root to resolve LSB and ELF interpreter issues with FlexNet and recent RHEL-based distributions.

```
cd /lib64
ln -s ld-linux-x86-64.so.2 ld-lsb-x86-64.so.3
semanage fcontext -a -f l -t ld_so_t "/usr/lib/ld-[^/]*\.so(\.[^/]*)*"
restorecon -v /lib64/ld-lsb-x86-64.so.3
```


### Step. 0 : Prepare FlexNet file

The file structure should be as follows.

- `/usr/local/bin/lmgrd` (file) : FletNet service
- `/usr/local/bin/lmutil` (file) : FletNet utilities
- `/usr/local/lib/flexnet/` (dir) : Directory for vendor files
- `/usr/local/etc/flexnet/` (dir) : Directory for license files

### Step. 1 : Add DNF repository

Execute the following command as root

```sh
dnf config-manager --add-repo https://raw.githubusercontent.com/Mine02C4/flexnet_selinux/main/repo/flexnet_selinux.repo
```

If you want to import GPG keys in advance, execute the following command. (Optional)

```sh
rpm --import https://raw.githubusercontent.com/Mine02C4/flexnet_selinux/main/signature/public.gpg
```

### Step. 2 : Install package

Execute the following command as root

```sh
dnf install flexnet_selinux
```

If you run the command for the first time without importing the GPG key, the fingerprint of the GPG key will be confirmed. Please check if it matches the following.

```
Userid     : "NIWA Naoya (flexnet_selinux) <mine@mine02c4.nagoya>"
Fingerprint: 7C91 B554 3F5E 0ACA C081 264F BE25 99DD B245 DCE6
From       : https://raw.githubusercontent.com/Mine02C4/flexnet_selinux/main/signature/public.gpg
```

### Additional step : Relabel

If the policy was installed prior to FlexNet configuration, it will need to relabel. Please relabel with the following command.

```sh
restorecon -F -R -i -v /usr/local/bin/lmgrd
restorecon -F -R -i -v /usr/local/bin/lmutil
restorecon -F -R -i -v /usr/local/lib/flexnet
restorecon -F -R -i -v /usr/local/etc/flexnet
```
