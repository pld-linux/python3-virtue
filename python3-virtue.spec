#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Modern, extensible, unittest compliant test runner
Summary(pl.UTF-8):	Nowoczesne, rozszerzalne, zgodne z unittest narzędzie do uruchamiania testów
Name:		python3-virtue
Version:	2025.7.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/virtue/
Source0:	https://files.pythonhosted.org/packages/source/v/virtue/virtue-%{version}.tar.gz
# Source0-md5:	cb9fa2b248a7e4477dc6e9778f7281be
URL:		https://pypi.org/project/virtue/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
%if %{with tests}
BuildRequires:	python3-attrs >= 22.2.0
BuildRequires:	python3-click
BuildRequires:	python3-colorama
BuildRequires:	python3-pyrsistent
BuildRequires:	python3-twisted >= 23.10
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.042
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-pyenchant >= 3.3
BuildRequires:	python3-pygments-github-lexers
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinxcontrib-spelling
BuildRequires:	python3-sphinxext.opengraph
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtue is a modern, extensible, unittest
(<https://docs.python.org/3/library/unittest.html>) compliant test
runner.

%description -l pl.UTF-8
virtue to nowoczesne, rozszerzalne, zgodne z unittest
(<https://docs.python.org/3/library/unittest.html>) narzędzie do
uruchamiania testów.

%package apidocs
Summary:	API documentation for Python virtue module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona virtue
Group:		Documentation

%description apidocs
API documentation for Python virtue module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona virtue.

%prep
%setup -q -n virtue-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m virtue virtue.tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-test

PYTHONPATH=$(pwd)/build-3-test \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/virtue{,-3}
ln -s virtue-3 $RPM_BUILD_ROOT%{_bindir}/virtue

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/virtue/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%attr(755,root,root) %{_bindir}/virtue-3
%{_bindir}/virtue
%{py3_sitescriptdir}/virtue
%{py3_sitescriptdir}/virtue-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
