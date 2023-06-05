// import orderBy from 'lodash/orderBy';
import { EventInput } from '@fullcalendar/core';
// @mui
import { DatePicker } from '@mui/x-date-pickers';
import { Box, Stack, Tooltip, TextField, IconButton } from '@mui/material';
// utils

// components
import Iconify from '../../../components/iconify';

// ----------------------------------------------------------------------

type Props = {
  lessons: EventInput[];
  onResetFilter: VoidFunction;
  startDate: Date | null;
  endDate: Date | null;
  setStartDate: (value: Date | null) => void;
  setEndDate: (value: Date | null) => void;
  onSelectLesson: (lessonId: string) => void;
};

export default function CalendarFilterDrawer({
  startDate,
  endDate,
  setStartDate,
  setEndDate,
  onResetFilter,
}: Props) {
  return (
    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1}>
      <DatePicker
        label="Start date"
        value={startDate}
        onChange={setStartDate}
        renderInput={(params) => <TextField size="small" {...params} />}
      />

      <DatePicker
        label="End date"
        value={endDate}
        onChange={setEndDate}
        renderInput={(params) => <TextField size="small" {...params} />}
      />

      <Tooltip title="Reset date">
        <Box sx={{ position: 'relative' }}>
          <IconButton onClick={onResetFilter}>
            <Iconify icon="ic:round-refresh" />
          </IconButton>
        </Box>
      </Tooltip>
    </Stack>
  );
}
