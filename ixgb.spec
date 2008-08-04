# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%ifarch sparc
%undefine	with_smp
%endif

%if %{without kernel}
%undefine with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		rel	9
%define		pname	ixgb
Summary:	Intel(R) 10 Gigabit driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) 10 Gigabit
Name:		%{pname}%{_alt_kernel}
Version:	1.0.135
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/e1000/%{pname}-%{version}.tar.gz
# Source0-md5:	400ec2e8477cd43db253e5ed067b6ec4
URL:		http://sourceforge.net/projects/e1000/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) 10 Gigabit
adapters.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Intel(R) 10 Gigabit.

%package -n kernel%{_alt_kernel}-net-ixgb
Summary:	Intel(R) 10 Gigabit driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) 10 Gigabit
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-ixgb
This package contains the Linux driver for the Intel(R) 10 Gigabit
adapters.

%description -n kernel%{_alt_kernel}-net-ixgb -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Intel(R) 10 Gigabit.

%prep
%setup -q -n %{pname}-%{version}
cat > src/Makefile <<'EOF'
obj-m := ixgb.o
ixgb-objs := ixgb_ee.o ixgb_hw.o ixgb_param.o ixgb_ethtool.o \
ixgb_main.o kcompat.o

EXTRA_CFLAGS=-DDRIVER_IXGB
EOF

%build
%build_kernel_modules -C src -m %{pname}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/%{pname} -d kernel/drivers/net -n %{pname} -s current
# blacklist kernel module
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf <<'EOF'
blacklist ixgb
alias ixgb ixgb-current
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-ixgb
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-ixgb
%depmod %{_kernel_ver}

%files	-n kernel%{_alt_kernel}-net-ixgb
%defattr(644,root,root,755)
%doc ixgb.7 README
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*
