import { Link } from 'react-router-dom';
// @mui
import { Stack, Checkbox, TableRow, TableCell, Typography } from '@mui/material';
// @types
import { IPayslip } from '../../../../@types/payslip';
//formating
import { fDate } from '../../../../utils/formatTime';
import { fCurrency } from '../../../../utils/formatNumber';
// ----------------------------------------------------------------------

type Props = {
  row: IPayslip;
  selected: boolean;
  onSelectRow: VoidFunction;
  onDeleteRow: VoidFunction;
};

export default function PayslipTableRow({ row, selected, onSelectRow, onDeleteRow }: Props) {
  const { id, teacher_id, start_date, end_date, amount, hours, created_at } = row;

  return (
    <>
      <TableRow hover selected={selected}>
        <TableCell padding="checkbox">
          <Checkbox checked={selected} onClick={onSelectRow} />
        </TableCell>

        <TableCell>
          <Link
            to={`/payslip/${teacher_id}/${id}`}
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            <Stack direction="row" alignItems="center" spacing={2}>
              <Typography variant="subtitle2" noWrap>
                {id}
              </Typography>
            </Stack>
          </Link>
        </TableCell>

        <TableCell align="left">
          <Link to={`/tutor/${teacher_id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            {teacher_id}
          </Link>
        </TableCell>

        <TableCell align="left" sx={{ textTransform: 'capitalize' }}>
          {fDate(start_date, 'dd MMM yyyy')}
        </TableCell>

        <TableCell align="left" sx={{ textTransform: 'capitalize' }}>
          {fDate(end_date, 'dd MMM yyyy')}
        </TableCell>

        <TableCell align="left">{fCurrency(amount)} DKK</TableCell>

        <TableCell align="left">{hours}</TableCell>
      </TableRow>
    </>
  );
}
