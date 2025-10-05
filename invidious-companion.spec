%global debug_package        %{nil}
%global __strip              /usr/bin/true
%global __objcopy            /usr/bin/true
%global git_commit_sha       0065a3e42bde974c728605ba7040b20df885cb68
%global git_commit_timestamp 20250929000000


Name:           invidious-companion
Version:        0.1.%{git_commit_timestamp}
Release:        %autorelease
Summary:        Invidious companion for handling video streams - based on youtube.js
License:        AGPLv3
URL:            https://github.com/iv-org/invidious-companion
Source0:        https://github.com/iv-org/invidious-companion/archive/%{git_commit_sha}.tar.gz
Source1:        %{name}.env
Source2:        %{name}-service.preset


ExclusiveArch: x86_64 aarch64


BuildRequires: crudini
BuildRequires: deno-bin
BuildRequires: systemd-rpm-macros


%{?systemd_requires}
%{?sysusers_requires_compat}


%description
%{summary}.


%prep
%setup -q -n %{name}-%{git_commit_sha}


%build
deno run compile \
  --include ./src/lib/helpers/youtubePlayerReq.ts \
  --include ./src/lib/helpers/getFetchClient.ts \
  src/main.ts \
  --_version_commit="%{git_commit_sha}"


%install
install --mode=750 --directory "%{buildroot}%{_sysconfdir}/invidious-companion"
install --mode=640 config/config.example.toml "%{buildroot}%{_sysconfdir}/invidious-companion/config.example.toml"
install -D --mode=755 invidious_companion "%{buildroot}%{_libexecdir}/invidious_companion"
install -D --mode=644 invidious-companion.service "%{buildroot}%{_unitdir}/%{name}.service"
install -D --mode=644 "%{SOURCE1}" "%{buildroot}%{_sysconfdir}/default/invidious-companion"
install -D --mode=644 "%{SOURCE2}" "%{buildroot}%{_prefix}/lib/systemd/system-preset/90-invidious-companion.preset"

crudini --del --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service BindPaths
crudini --del --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service BindReadOnlyPaths
crudini --del --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service Environment
crudini --set --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service BindPaths %{_sharedstatedir}/invidious-companion
crudini --set --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service ExecStart %{_libexecdir}/invidious_companion
crudini --set --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service Group invidious-companion
crudini --set --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service Restart on-failure
crudini --set --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service User invidious-companion
crudini --set --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service WorkingDirectory %{_sharedstatedir}/invidious-companion
crudini --set --inplace "%{buildroot}%{_unitdir}/%{name}.service" Service EnvironmentFile %{_sysconfdir}/default/invidious-companion


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
