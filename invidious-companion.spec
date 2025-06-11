%global debug_package        %{nil}
%global __strip              /usr/bin/true
%global __objcopy            /usr/bin/true
%global git_commit_sha       d0c4bb79ae4688d019fb281257859e334adb7d8b
%global git_commit_timestamp 20250609205554


Name:           invidious-companion
Version:        0.1.%{git_commit_timestamp}
Release:        %autorelease
Summary:        Invidious companion for handling video streams - based on youtube.js
License:        AGPLv3
URL:            https://github.com/iv-org/invidious-companion
Source0:        https://github.com/iv-org/invidious-companion/archive/%{git_commit_sha}.tar.gz
Source1:        %{name}.env
Source2:        %{name}.service
Source3:        %{name}-service.preset


ExclusiveArch: x86_64 aarch64


BuildRequires: deno-bin
BuildRequires: systemd-rpm-macros


%{?systemd_requires}
%{?sysusers_requires_compat}


%description
%{summary}.


%prep
%setup -q -n %{name}-%{git_commit_sha}


%build
deno run compile


%install
install --mode=750 --directory "%{buildroot}%{_sysconfdir}/invidious-companion"
install --mode=640 config/config.example.toml "%{buildroot}%{_sysconfdir}/invidious-companion/config.example.toml"
install -D --mode=644 "%{SOURCE1}" "%{buildroot}%{_sysconfdir}/default/invidious-companion"
install -D --mode=755 invidious_companion "%{buildroot}%{_libexecdir}/invidious_companion"
install -D --mode=644 "%{SOURCE2}" "%{buildroot}%{_unitdir}/%{name}.service"
install -D --mode=644 "%{SOURCE3}" "%{buildroot}%{_prefix}/lib/systemd/system-preset/90-invidious-companion.preset"


%files
%doc README.md
%license LICENSE
%defattr(0640,root,invidious-companion,0750)
%dir %{_sysconfdir}/invidious-companion
%{_sysconfdir}/invidious-companion/config.example.toml
%defattr(-,root,root,-)
%{_sysconfdir}/default/invidious-companion
%{_libexecdir}/invidious_companion
%{_unitdir}/%{name}.service
%{_prefix}/lib/systemd/system-preset/90-invidious-companion.preset


%pre
getent group invidious-companion > /dev/null || groupadd --system invidious-companion
getent passwd invidious-companion > /dev/null || \
  useradd --system --create-home --home-dir "%{_sharedstatedir}/invidious-companion" --gid invidious-companion \
  -s /sbin/nologin -c "invidious-companion daemon" invidious-companion
exit 0


%post
%systemd_post invidious-companion.service


%preun
%systemd_preun invidious-companion.service


%postun
%systemd_postun invidious-companion.service


%changelog
%autochangelog
