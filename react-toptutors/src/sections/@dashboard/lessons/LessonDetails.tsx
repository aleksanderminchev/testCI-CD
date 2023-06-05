/* follow this path to see where the inspiration for this code comes from in the Minimal_TypeScript_v4.2.0:

src/sections/@dashboard/general/booking/BookingDetails
*/

import { format } from 'date-fns';
import { sentenceCase } from 'change-case';
// @mui
import { useTheme } from '@mui/material/styles';

import { useState } from 'react';

import {
  Card,
  Stack,
  Table,
  Divider,
  TableRow,
  TableBody,
  TableCell,
  CardProps,
  CardHeader,
  Typography,
  TableContainer,
  Avatar,
} from '@mui/material';

import { PATH_DASHBOARD } from '../../../routes/paths';

// components
import Label from '../../../components/label';

import Scrollbar from '../../../components/scrollbar';

import { TableHeadCustom } from '../../../components/table';

import NavigateButton from '../components/NavigateButton';

// ----------------------------------------------------------------------

type RowProps = {
  id: string;
  avatar: string;
  student: string;
  date: Date;
  startTime: Date;
  endTime: Date;
  duration: number;
  status: string;
  wage: number;
  paid: string;
};

interface Props extends CardProps {
  title?: string;
  subheader?: string;
  tableLabels: any;
  tableData: RowProps[];
}

export default function BookingDetails({
  title,
  subheader,
  tableLabels,
  tableData,
  ...other
}: Props) {
  const [openLessonsList, setOpenLessonsList] = useState(false);

  const handleOpenLessonsList = () => {
    setOpenLessonsList(true);
  };

  return (
    <Card {...other}>
      <CardHeader title={title} subheader={subheader} sx={{ mt: 3 }} />

      <NavigateButton
        link={PATH_DASHBOARD.lesson.root}
        onOpen={handleOpenLessonsList}
        sx={{ mb: 5 }}
      />

      <TableContainer sx={{ overflow: 'unset' }}>
        <Scrollbar>
          <Table sx={{ minWidth: 960 }}>
            <TableHeadCustom headLabel={tableLabels} />

            <TableBody>
              {tableData.map((row) => (
                <BookingDetailsRow key={row.id} row={row} />
              ))}
            </TableBody>
          </Table>
        </Scrollbar>
      </TableContainer>

      <Divider />
    </Card>
  );
}

// ----------------------------------------------------------------------

type BookingDetailsRowProps = {
  row: RowProps;
};

function BookingDetailsRow({ row }: BookingDetailsRowProps) {
  const theme = useTheme();

  const isLight = theme.palette.mode === 'light';

  row.duration = row.endTime.getHours() - row.startTime.getHours();

  return (
    <TableRow>
      <TableCell>
        <Stack direction="row" alignItems="center" spacing={2}>
          <Avatar alt={row.student} src={row.avatar} />

          <Typography variant="subtitle2" noWrap>
            {row.student}
          </Typography>
        </Stack>
      </TableCell>

      <TableCell>
        <Typography variant="subtitle2">{format(new Date(row.date), 'dd MMM yyyy')}</Typography>
      </TableCell>

      <TableCell>{format(new Date(row.startTime.setHours(18)), 'p')}</TableCell>
      <TableCell>{format(new Date(row.endTime.setHours(20)), 'p')}</TableCell>

      <TableCell>
        <Label
          variant={isLight ? 'soft' : 'filled'}
          color={
            (row.status === 'paid' && 'success') ||
            (row.status === 'pending' && 'warning') ||
            'error'
          }
        >
          {sentenceCase(row.status)}
        </Label>
      </TableCell>

      <TableCell>{row.endTime.getHours() - row.startTime.getHours()}</TableCell>

      <TableCell sx={{ textTransform: 'capitalize' }}>{row.wage}</TableCell>
    </TableRow>
  );
}
