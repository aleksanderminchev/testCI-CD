import { Link as RouterLink } from 'react-router-dom';
// @mui
import {
  Box,
  Card,
  Stack,
  Avatar,
  Tooltip,
  CardProps,
  Typography,
  CardHeader,
  IconButton,
} from '@mui/material';
// components
import Iconify from '../../../components/iconify';
import { PATH_DASHBOARD } from '../../../routes/paths';

// ----------------------------------------------------------------------

interface Props extends CardProps {
  title?: string;
  subheader?: string;
  isTeacher: boolean;
  list: {
    id: string;
    name: string;
    email: string;
    avatar: string;
    phone: string;
  }[];
}

export default function AppContacts({ title, isTeacher, subheader, list, ...other }: Props) {
  return (
    <Card {...other}>
      <CardHeader
        title={title}
        subheader={subheader}
        // Should lead you to a form to get an extra tutor.
        // action={
        //   <Tooltip title="Add Contact">
        //     <IconButton color="primary" size="large">
        //       <Iconify icon="eva:plus-fill" />
        //     </IconButton>
        //   </Tooltip>
        // }
      />

      <Stack spacing={3} sx={{ p: 3 }}>
        {list.map((contact) => (
          <Stack direction="row" alignItems="center" key={contact.id}>
            <Avatar src={contact.avatar} sx={{ width: 48, height: 48 }} />

            <Box sx={{ flexGrow: 1, ml: 2, minWidth: 100 }}>
              <Typography variant="subtitle2" sx={{ mb: 0.5 }} noWrap>
                {contact.name}
              </Typography>

              <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                {contact.email}
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                {contact.phone}
              </Typography>
            </Box>

            <Tooltip title="Se profil">
              <IconButton
                component={RouterLink}
                to={
                  isTeacher
                    ? PATH_DASHBOARD.student.profile(contact.id)
                    : PATH_DASHBOARD.tutor.profile(contact.id)
                }
                size="small"
              >
                <Iconify icon="eva:diagonal-arrow-right-up-fill" />
              </IconButton>
            </Tooltip>
          </Stack>
        ))}
        {/* SHOULD BE A BUTTON TO REQUEST AN EXTRA TUTOR */}
        {/* <Button variant="outlined" size="large" color="inherit">
          View All
        </Button> */}
      </Stack>
    </Card>
  );
}
