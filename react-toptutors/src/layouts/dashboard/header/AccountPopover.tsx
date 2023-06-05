import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// @mui
import { alpha } from '@mui/material/styles';
import { Box, Divider, Typography, Stack, MenuItem } from '@mui/material';
// routes
import { PATH_AUTH } from '../../../routes/paths';
import { PATH_DASHBOARD } from '../../../routes/paths';

// auth
import { useAuthContext } from '../../../auth/useAuthContext';
// components
import { CustomAvatar } from '../../../components/custom-avatar';
import { useSnackbar } from '../../../components/snackbar';
import MenuPopover from '../../../components/menu-popover';
import { IconButtonAnimate } from '../../../components/animate';

// ----------------------------------------------------------------------

type Role = 'admin' | 'customer' | 'student' | 'teacher';

export default function AccountPopover() {
  const navigate = useNavigate();

  const { user, logout } = useAuthContext();
  console.log(user);
  // Options for everyone
  const baseOptions = [
    {
      label: 'Oversigt 🔍',
      linkTo: '/',
    },
    {
      label: 'Kalender 📅',
      linkTo: '/calendar',
    },
  ];

  // Options only for admins
  const adminOptions = [
    {
      label: 'Admin Dashboard',
      linkTo: '/admin',
    },
  ];

  // Options only for customers
  const customerOptions = [
    {
      label: 'Min Profil 🎓',
      linkTo: PATH_DASHBOARD.family.profile(user?.customer_dict?.id),
    },
  ];

  // Options only for students
  const studentOptions = [
    {
      label: 'Min Profil 🎓',
      linkTo: PATH_DASHBOARD.student.profile(user?.student_dict?.id),
    },
  ];

  // Options only for tutors
  const tutorOptions = [
    {
      label: 'Min Profil 🎓',
      linkTo: PATH_DASHBOARD.tutor.profile(user?.teacher_dict?.id),
    },
  ];

  const roleOptions: Record<Role, typeof baseOptions> = {
    admin: adminOptions,
    customer: customerOptions,
    student: studentOptions,
    teacher: tutorOptions,
  };

  const OPTIONS = [
    ...baseOptions,
    ...(user?.roles.flatMap((role: Role) => roleOptions[role] || []) ?? []),
  ];

  const { enqueueSnackbar } = useSnackbar();

  const [openPopover, setOpenPopover] = useState<HTMLElement | null>(null);

  const handleOpenPopover = (event: React.MouseEvent<HTMLElement>) => {
    setOpenPopover(event.currentTarget);
  };

  const handleClosePopover = () => {
    setOpenPopover(null);
  };

  const handleLogout = async () => {
    try {
      logout();
      navigate(PATH_AUTH.login, { replace: true });
      handleClosePopover();
    } catch (error) {
      console.error(error);
      enqueueSnackbar('Unable to logout!', { variant: 'error' });
    }
  };

  const handleClickItem = (path: string) => {
    handleClosePopover();
    navigate(path);
  };

  return (
    <>
      <IconButtonAnimate
        onClick={handleOpenPopover}
        sx={{
          p: 0,
          ...(openPopover && {
            '&:before': {
              zIndex: 1,
              content: "''",
              width: '100%',
              height: '100%',
              borderRadius: '50%',
              position: 'absolute',
              bgcolor: (theme) => alpha(theme.palette.grey[900], 0.8),
            },
          }),
        }}
      >
        <CustomAvatar
          src={user?.teacher_dict?.photo || ''}
          alt={user?.first_name}
          name={user?.first_name}
        />
      </IconButtonAnimate>

      <MenuPopover open={openPopover} onClose={handleClosePopover} sx={{ width: 200, p: 0 }}>
        <Box sx={{ my: 1.5, px: 2.5 }}>
          <Typography variant="subtitle2" noWrap>
            {user?.displayName}
          </Typography>

          <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
            {user?.email}
          </Typography>
        </Box>

        <Divider sx={{ borderStyle: 'dashed' }} />

        <Stack sx={{ p: 1 }}>
          {OPTIONS.map((option) => (
            <MenuItem key={option.label} onClick={() => handleClickItem(option.linkTo)}>
              {option.label}
            </MenuItem>
          ))}
        </Stack>

        <Divider sx={{ borderStyle: 'dashed' }} />

        <MenuItem onClick={handleLogout} sx={{ m: 1 }}>
          Log ud 👋
        </MenuItem>
      </MenuPopover>
    </>
  );
}
