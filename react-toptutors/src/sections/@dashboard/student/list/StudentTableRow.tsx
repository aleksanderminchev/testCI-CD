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
import { IStudent } from '../../../../@types/student';
// components
import Label from '../../../../components/label';
import Iconify from '../../../../components/iconify';
import MenuPopover from '../../../../components/menu-popover';
import ConfirmDialog from '../../../../components/confirm-dialog';

// ----------------------------------------------------------------------

type Props = {
  row: IStudent;
  selected: boolean;
  isAdmin: boolean;
  onEditRow: VoidFunction;
  onSelectRow: VoidFunction;
  onDeleteRow: VoidFunction;
};

export default function StudentTableRow({
  row,
  selected,
  isAdmin,
  onEditRow,
  onSelectRow,
  onDeleteRow,
}: Props) {
  const { id, first_name, last_name, email, phone, student_type, status } = row;

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
        {isAdmin ? (
          <TableCell padding="checkbox">
            <Checkbox checked={selected} onClick={onSelectRow} />
          </TableCell>
        ) : (
          <TableCell padding="checkbox"></TableCell>
        )}

        <TableCell>
          <Link to={`/student/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            <Stack direction="row" alignItems="center" spacing={2}>
              <Typography variant="subtitle2" noWrap>
                {first_name} {last_name}
              </Typography>
            </Stack>
          </Link>
        </TableCell>

        <TableCell align="left">
          <Link to={`/student/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            {email}
          </Link>
        </TableCell>

        <TableCell align="left" sx={{ textTransform: 'capitalize' }}>
          <Link to={`/student/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            {phone}
          </Link>
        </TableCell>

        {isAdmin ? (
          <>
            <TableCell align="left" sx={{ textTransform: 'capitalize' }}>
              <Link to={`/student/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                {student_type}
              </Link>
            </TableCell>

            <TableCell align="left">
              <Link to={`/student/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                <Label
                  variant="soft"
                  color={(status === 'inactive' && 'error') || 'success'}
                  sx={{ textTransform: 'capitalize' }}
                >
                  {status}
                </Label>
              </Link>
            </TableCell>
            <TableCell align="right">
              <IconButton color={openPopover ? 'inherit' : 'default'} onClick={handleOpenPopover}>
                <Iconify icon="eva:more-vertical-fill" />
              </IconButton>
            </TableCell>
          </>
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
