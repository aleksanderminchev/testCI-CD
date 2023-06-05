import { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useNavigate } from 'react-router';
// @mui
import {
  Box,
  Card,
  Table,
  Button,
  Divider,
  TableRow,
  TableBody,
  TableCell,
  CardProps,
  CardHeader,
  TableContainer,
} from '@mui/material';

import Scrollbar from '../../../components/scrollbar';
import { TableHeadCustom } from '../../../components/table';

// @types
import { ILesson } from '../../../@types/lesson';

// components
import Iconify from '../../../components/iconify';

// redux
import { useSelector } from '../../../redux/store';

import { fNumber } from '../../../utils/formatNumber';

// ----------------------------------------------------------------------

interface Props extends CardProps {
  heading?: string;
  link: string;
}

const TABLE_HEAD = [
  { id: 'title', label: 'Titel' },
  { id: 'tutor', label: 'Tutor' },
  { id: 'duration', label: 'Længde' },
  { id: 'join', label: '' },
];

export default function AppUpcomingLessons({ heading, link, ...other }: Props) {
  const { lessons, isLoading } = useSelector((state) => state.lesson);
  const [tableData, setTableData] = useState<ILesson[]>([]);

  useEffect(() => {
    if (lessons.length) {
      console.log(lessons);
      setTableData(lessons.slice(0, 5));
    }
  }, [lessons]);
  return (
    <Card {...other}>
      <CardHeader title={heading} sx={{ mb: 3 }} />
      <TableContainer sx={{ overflow: 'unset' }}>
        <Scrollbar>
          <Table sx={{ minWidth: 720 }}>
            <TableHeadCustom headLabel={TABLE_HEAD} />
            <TableBody>
              {tableData.map((row) => (
                <LessonRow key={row.id} row={row} />
              ))}
            </TableBody>
          </Table>
        </Scrollbar>
      </TableContainer>
      <Divider />
      <Box sx={{ p: 2, textAlign: 'right' }}>
        {link && (
          <Button
            to={link}
            component={RouterLink}
            size="small"
            color="inherit"
            endIcon={<Iconify icon="eva:chevron-right-fill" />}
          >
            Se alle lektioner
          </Button>
        )}
      </Box>
    </Card>
  );
}
// ----------------------------------------------------------------------

type LessonRowProps = {
  row: ILesson;
};

function LessonRow({ row }: LessonRowProps) {
  const { id, title, teacher, duration_in_minutes, status, from_time } = row;
  const navigate = useNavigate();

  const hours = Math.floor(duration_in_minutes / 60);
  const minutes = duration_in_minutes % 60;

  const formattedHours = fNumber(hours);
  const formattedMinutes = fNumber(minutes);

  const hourLabel = hours === 1 ? 'time' : 'timer';
  return (
    <>
      <TableRow key={id}>
        <TableCell>{title}</TableCell>
        <TableCell>{teacher.first_name}</TableCell>
        {/* <TableCell>
          {fNumber(duration_in_minutes / 60)} timer {fNumber(duration_in_minutes % 60)} minutter
        </TableCell> */}

        <TableCell>
          {hours !== 0 && `${formattedHours} ${hourLabel} `}
          {minutes !== 0 && `${formattedMinutes} minutter`}
        </TableCell>

        <TableCell>
          <Button
            variant="contained"
            size="medium"
            fullWidth
            onClick={() => {
              navigate(`/lesson/${id}`);
            }}
          >
            Tilslut nu
          </Button>
        </TableCell>
      </TableRow>
    </>
  );
}
