/* follow this path to see where the inspiration for this code comes from in the Minimal_TypeScript_v4.2.0:

src/sections/@dashboard/user/list/UserTableRow
*/

import { fDate } from '../../../utils/formatTime';
import { fCurrency, fNumber } from '../../../utils/formatNumber';
// @mui
import { Stack, TableRow, TableCell, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTheme } from '@mui/material/styles';

// @types
import { ILesson } from '../../../@types/lesson';
// components
import Label from '../../../components/label';
import { CustomAvatar } from '../../../components/custom-avatar';

// ----------------------------------------------------------------------

type Props = {
  row: ILesson;
};

export default function UserTableRow({ row }: Props) {
  const { student, teacher, from_time, to_time, status, duration_in_minutes, wage, paid } = row;

  const theme = useTheme();
  const isLight = theme.palette.mode === 'light';

  return (
    <TableRow>
      <TableCell>
        <Link to={`/student/${student.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <CustomAvatar src={''} alt={student?.first_name} name={student?.first_name} />
            <Typography variant="subtitle2" noWrap>
              {student.first_name} {student.last_name}
            </Typography>
          </Stack>
        </Link>
      </TableCell>

      <TableCell align="left">{fDate(from_time, 'dd MMM yyyy')}</TableCell>

      <TableCell align="left">{fDate(from_time, 'hh:mm')}</TableCell>

      <TableCell align="left">{fDate(to_time, 'hh:mm')}</TableCell>

      <TableCell align="left">
        <Label
          variant={isLight ? 'soft' : 'filled'}
          color={
            (status === 'attended' && 'success') || (status === 'scheduled' && 'warning') || 'error'
          }
          sx={{ textTransform: 'capitalize' }}
        >
          {status}
        </Label>
      </TableCell>

      <TableCell>
        {fNumber(duration_in_minutes / 60)}:{fNumber(duration_in_minutes % 60)}
      </TableCell>
      <TableCell sx={{ textTransform: 'capitalize' }}> {fCurrency(wage)}DKK</TableCell>
      <TableCell sx={{ textTransform: 'capitalize' }}>
        <Label
          variant={isLight ? 'soft' : 'filled'}
          color={paid ? 'success' : 'error'}
          sx={{ textTransform: 'capitalize' }}
        >
          {paid ? 'Paid out' : 'Not Paid out'}
        </Label>
      </TableCell>
    </TableRow>
  );
}
