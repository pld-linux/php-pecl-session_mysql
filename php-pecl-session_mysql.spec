%define		_modname	session_mysql
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	MySQL session save handler for PHP
Name:		php-pecl-%{_modname}
Version:	1.8
Release:	0.4
License:	MIT
Group:		Development/Languages/PHP
Source0:	http://websupport.sk/~stanojr/projects/session_mysql/%{_modname}-%{version}.tgz
# Source0-md5:	d3507e1a9d0a82412cc2b5c673aa8ca1
Source1:	%{name}.ini
Source2:	%{name}.sql
Patch0:		%{name}-zts.patch
URL:		http://websupport.sk/~stanojr/projects/session_mysql/
BuildRequires:	mysql-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Requires:	php-mysql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL session save handler for PHP.
- supports locking
- very quiet (doesnt log any error) (but upper session functions can
  print some error).

%prep
%setup -q -n %{_modname}-%{version}
%patch0 -p1
cp -a %{SOURCE2} database.sql

%build
phpize
%configure \
	--with-mysql=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc LICENCE README database.sql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
