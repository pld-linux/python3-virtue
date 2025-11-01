#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (some files missing in sdist)
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-virtue.spec)

Summary:	Modern, extensible, unittest compliant test runner
Summary(pl.UTF-8):	Nowoczesne, rozszerzalne, zgodne z unittest narzędzie do uruchamiania testów
Name:		python-virtue
# keep 1.0.x here for python2 support
Version:	1.0.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/virtue/
Source0:	https://files.pythonhosted.org/packages/source/v/virtue/virtue-%{version}.tar.gz
# Source0-md5:	7eec6d1a3b9b16320dd6981272ca3f03
URL:		https://pypi.org/project/virtue/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:40.6.0
BuildRequires:	python-setuptools_scm >= 3.4
BuildRequires:	python-toml
%if %{with tests}
BuildRequires:	python-attrs >= 19
BuildRequires:	python-click
BuildRequires:	python-colorama
BuildRequires:	python-importlib_metadata
BuildRequires:	python-pyrsistent
BuildRequires:	python-twisted
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:40.6.0
BuildRequires:	python3-setuptools_scm >= 3.4
%if %{with tests}
BuildRequires:	python3-attrs >= 19
BuildRequires:	python3-click
BuildRequires:	python3-colorama
%if "%{_ver_lt %{py3_ver} 3.8}" == "1"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-pyrsistent
BuildRequires:	python3-twisted
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-pygments-github-lexers
BuildRequires:	python-sphinxcontrib-spelling
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-virtue
Summary:	Modern, extensible, unittest compliant test runner
Summary(pl.UTF-8):	Nowoczesne, rozszerzalne, zgodne z unittest narzędzie do uruchamiania testów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-virtue
virtue is a modern, extensible, unittest
(<https://docs.python.org/3/library/unittest.html>) compliant test
runner.

%description -n python3-virtue -l pl.UTF-8
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

# stub for setuptools
cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python} -m virtue virtue.tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m virtue virtue.tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/virtue{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/virtue{,-3}
ln -s virtue-3 $RPM_BUILD_ROOT%{_bindir}/virtue
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%attr(755,root,root) %{_bindir}/virtue-2
%{py_sitescriptdir}/virtue
%{py_sitescriptdir}/virtue-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-virtue
%defattr(644,root,root,755)
%doc COPYING README.rst
%attr(755,root,root) %{_bindir}/virtue-3
%{_bindir}/virtue
%{py3_sitescriptdir}/virtue
%{py3_sitescriptdir}/virtue-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
