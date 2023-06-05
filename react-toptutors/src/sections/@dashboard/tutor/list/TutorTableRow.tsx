import { useState } from 'react';
import { Link } from 'react-router-dom';
// @mui
import {
  Stack,
  Button,
  Checkbox,
  TableRow,
  MenuItem,
  TableCell,
  IconButton,
  Typography,
} from '@mui/material';
// @types
import { ITutor } from '../../../../@types/tutor';
// components
import Label from '../../../../components/label';
import Iconify from '../../../../components/iconify';
import MenuPopover from '../../../../components/menu-popover';
import ConfirmDialog from '../../../../components/confirm-dialog';

// ----------------------------------------------------------------------

type Props = {
  row: ITutor;
  selected: boolean;
  onEditRow: VoidFunction;
  onSelectRow: VoidFunction;
  onDeleteRow: VoidFunction;
  isAdmin: boolean;
};

export default function TutorTableRow({
  row,
  selected,
  onEditRow,
  onSelectRow,
  onDeleteRow,
  isAdmin,
}: Props) {
  const { id, first_name, last_name, email, phone, status, open_for_new_students } = row;

  const [openConfirm, setOpenConfirm] = useState(false);

  const [openPopover, setOpenPopover] = useState<HTMLElement | null>(null);

  const handleOpenConfirm = () => {
    setOpenConfirm(true);
  };

  const handleCloseConfirm = () => {
    setOpenConfirm(false);
  };

  const handleOpenPopover = (event: React.MouseEvent<HTMLElement>) => {
    setOpenPopover(event.currentTarget);
  };

  const handleClosePopover = () => {
    setOpenPopover(null);
  };

  return (
    <>
      <TableRow hover selected={selected}>
        <TableCell padding="checkbox">
          <Checkbox checked={selected} onClick={onSelectRow} />
        </TableCell>

        <TableCell>
          <Link to={`/tutor/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            <Stack direction="row" alignItems="center" spacing={2}>
              {/* <Avatar alt={first_name} src={avatarUrl} /> */}

              <Typography variant="subtitle2" noWrap>
                {first_name} {last_name}
              </Typography>
            </Stack>
          </Link>
        </TableCell>

        <TableCell align="left">
          <Link to={`/tutor/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            {email}
          </Link>
        </TableCell>

        <TableCell align="left" sx={{ textTransform: 'capitalize' }}>
          <Link to={`/tutor/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            {phone}
          </Link>
        </TableCell>

        <TableCell align="center">
          <Iconify
            icon={open_for_new_students ? 'eva:checkmark-circle-fill' : 'eva:alert-circle-outline'}
            sx={{
              width: 20,
              height: 20,
              color: 'success.main',
              ...(!open_for_new_students && { color: 'warning.main' }),
            }}
          />
        </TableCell>

        <TableCell align="left">
          <Link to={`/tutor/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            <Label
              variant="soft"
              color={
                (status === 'inactive' && 'error') ||
                (status === 'prospective' && 'warning') ||
                'success'
              }
              sx={{ textTransform: 'capitalize' }}
            >
              {status}
            </Label>
          </Link>
        </TableCell>
        {isAdmin ? (
          <TableCell align="right">
            <IconButton color={openPopover ? 'inherit' : 'default'} onClick={handleOpenPopover}>
              <Iconify icon="eva:more-vertical-fill" />
            </IconButton>
          </TableCell>
        ) : (
          <></>
        )}
      </TableRow>
      {isAdmin ? (
        <MenuPopover
          open={openPopover}
          onClose={handleClosePopover}
          arrow="right-top"
          sx={{ width: 140 }}
        >
          <MenuItem
            onClick={() => {
              handleOpenConfirm();
              handleClosePopover();
            }}
            sx={{ color: 'error.main' }}
          >
            <Iconify icon="eva:trash-2-outline" />
            Delete
          </MenuItem>

          <MenuItem
            onClick={() => {
              onEditRow();
              handleClosePopover();
            }}
          >
            <Iconify icon="eva:edit-fill" />
            Rediger
          </MenuItem>
        </MenuPopover>
      ) : (
        <></>
      )}
      <ConfirmDialog
        open={openConfirm}
        onClose={handleCloseConfirm}
        title="Delete"
        content="Are you sure want to delete?"
        action={
          <Button variant="contained" color="error" onClick={onDeleteRow}>
            Delete
          </Button>
        }
      />
    </>
  );
}
